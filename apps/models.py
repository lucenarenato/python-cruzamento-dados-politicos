# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class RISK_LEVEL(Enum):
    baixo = 'baixo'
    medio = 'medio'
    alto = 'alto'
    critico = 'critico'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    @classmethod
    def get_list(cls):
        return cls.query.all()

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class Sancao(db.Model):
    """Modelo para armazenar sanções do CEIS e outras bases"""
    
    __tablename__ = 'sancoes'

    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(14), nullable=False, index=True)
    nome_sancionado = db.Column(db.String(256), nullable=False)
    tipo_pessoa = db.Column(db.String(20))  # 'PF' ou 'PJ'
    tipo_sancao = db.Column(db.String(100))  # CEIS, CNEP, CEPIM, etc
    orgao_sancionador = db.Column(db.String(256))
    data_inicio_sancao = db.Column(db.Date)
    data_fim_sancao = db.Column(db.Date)
    motivo = db.Column(db.Text)
    fonte = db.Column(db.String(50))  # 'CEIS', 'CNEP', etc
    data_importacao = db.Column(db.DateTime, default=dt.datetime.utcnow)
    
    def __repr__(self):
        return f"<Sancao {self.nome_sancionado} - {self.tipo_sancao}>"
    
    @classmethod
    def find_by_cpf_cnpj(cls, documento: str) -> list:
        return cls.query.filter_by(cpf_cnpj=documento).all()
    
    @classmethod
    def get_active_sanctions(cls):
        hoje = dt.date.today()
        return cls.query.filter(
            cls.data_inicio_sancao <= hoje,
            db.or_(
                cls.data_fim_sancao >= hoje,
                cls.data_fim_sancao == None
            )
        ).all()


class Contrato(db.Model):
    """Modelo para armazenar contratos públicos"""
    
    __tablename__ = 'contratos'

    id = db.Column(db.Integer, primary_key=True)
    numero_contrato = db.Column(db.String(100))
    cpf_cnpj_contratado = db.Column(db.String(14), nullable=False, index=True)
    nome_contratado = db.Column(db.String(256), nullable=False)
    orgao_contratante = db.Column(db.String(256))
    objeto = db.Column(db.Text)
    valor = db.Column(db.Numeric(15, 2))
    data_assinatura = db.Column(db.Date)
    data_inicio_vigencia = db.Column(db.Date)
    data_fim_vigencia = db.Column(db.Date)
    fonte = db.Column(db.String(50))  # 'PNCP', 'ComprasNet', etc
    url_fonte = db.Column(db.String(512))
    data_importacao = db.Column(db.DateTime, default=dt.datetime.utcnow)
    
    def __repr__(self):
        return f"<Contrato {self.numero_contrato} - {self.nome_contratado}>"
    
    @classmethod
    def find_by_cpf_cnpj(cls, documento: str) -> list:
        return cls.query.filter_by(cpf_cnpj_contratado=documento).all()
    
    @classmethod
    def get_recent_contracts(cls, days: int = 30):
        desde = dt.date.today() - dt.timedelta(days=days)
        return cls.query.filter(cls.data_assinatura >= desde).all()


class AlertaIntegridade(db.Model):
    """Alertas de possíveis irregularidades detectadas"""
    
    __tablename__ = 'alertas_integridade'

    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(14), nullable=False, index=True)
    nome = db.Column(db.String(256))
    tipo_alerta = db.Column(db.String(100))  # 'contrato_durante_sancao', 'evolucao_patrimonial', etc
    nivel_risco = db.Column(db.Enum(RISK_LEVEL), default=RISK_LEVEL.medio)
    descricao = db.Column(db.Text)
    dados_json = db.Column(db.JSON)  # Dados estruturados do alerta
    revisado = db.Column(db.Boolean, default=False)
    data_deteccao = db.Column(db.DateTime, default=dt.datetime.utcnow)
    
    def __repr__(self):
        return f"<Alerta {self.tipo_alerta} - {self.nome}>"
    
    @classmethod
    def get_unreviewed(cls):
        return cls.query.filter_by(revisado=False).order_by(cls.data_deteccao.desc()).all()
    
    @classmethod
    def get_by_risk_level(cls, nivel: RISK_LEVEL):
        return cls.query.filter_by(nivel_risco=nivel).all()


class PoliticoProfile(db.Model):
    """Perfil consolidado de políticos com dados do TSE e outras fontes"""
    
    __tablename__ = 'politicos'

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(256), nullable=False)
    nome_urna = db.Column(db.String(256))
    partido = db.Column(db.String(50))
    cargo = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    ano_eleicao = db.Column(db.Integer)
    situacao = db.Column(db.String(50))  # Eleito, Suplente, Não Eleito
    
    # Dados patrimoniais
    bens_declarados = db.Column(db.JSON)  # Lista de bens por ano
    total_bens_valor = db.Column(db.Numeric(15, 2))
    
    # Dados de doações
    doacoes_recebidas = db.Column(db.JSON)
    total_doacoes = db.Column(db.Numeric(15, 2))
    
    # Vínculos empresariais
    empresas_vinculadas = db.Column(db.JSON)  # QSA da Receita
    
    # Metadados
    fonte_tse = db.Column(db.String(256))
    ultima_atualizacao = db.Column(db.DateTime, default=dt.datetime.utcnow)
    
    def __repr__(self):
        return f"<Politico {self.nome} - {self.cargo}>"
    
    @classmethod
    def find_by_cpf(cls, cpf: str):
        return cls.query.filter_by(cpf=cpf).first()
    
    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(situacao='Eleito').all()

class ConsultaIntegridade(db.Model):
    """Histórico de consultas feitas através do monitor de integridade"""
    
    __tablename__ = 'consultas_integridade'

    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(14), nullable=False, index=True)
    tipo_documento = db.Column(db.String(3), nullable=False)  # 'CPF' ou 'CNPJ'
    
    # Resultado da consulta
    nivel_risco = db.Column(db.Enum(RISK_LEVEL), nullable=False)
    encontrado_ceis = db.Column(db.Boolean, default=False)
    encontrado_portal = db.Column(db.Boolean, default=False)
    
    # Dados detalhados (JSON para flexibilidade)
    dados_ceis = db.Column(db.JSON)  # Lista de registros CEIS encontrados
    dados_portal = db.Column(db.JSON)  # Dados do Portal da Transparência
    resultado_completo = db.Column(db.JSON)  # Resultado completo da análise
    
    # Metadados da consulta
    data_consulta = db.Column(db.DateTime, default=dt.datetime.utcnow, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_origem = db.Column(db.String(45))  # IPv4 ou IPv6
    
    def __repr__(self):
        return f"<ConsultaIntegridade {self.cpf_cnpj} - {self.nivel_risco.value} - {self.data_consulta}>"
    
    @classmethod
    def find_by_cpf_cnpj(cls, documento: str) -> list:
        """Retorna todas as consultas para um documento"""
        if not documento or not isinstance(documento, str) or len(documento.strip()) == 0:
            return []
        return cls.query.filter_by(cpf_cnpj=documento.strip()).order_by(cls.data_consulta.desc()).all()
    
    @classmethod
    def get_recent(cls, dias: int = 30) -> list:
        """Retorna consultas dos últimos N dias"""
        desde = dt.datetime.utcnow() - dt.timedelta(days=dias)
        return cls.query.filter(cls.data_consulta >= desde).order_by(cls.data_consulta.desc()).all()
    
    @classmethod
    def get_by_risk_level(cls, nivel: RISK_LEVEL) -> list:
        """Retorna consultas com determinado nível de risco"""
        return cls.query.filter_by(nivel_risco=nivel).order_by(cls.data_consulta.desc()).all()
    
    def save(self) -> None:
        """Salva a consulta no banco de dados"""
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)