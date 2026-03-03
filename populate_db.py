#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from apps import create_app, db
from apps.models import Sancao, Contrato, AlertaIntegridade, PoliticoProfile, RISK_LEVEL
from datetime import date, datetime
from decimal import Decimal


def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados"""
    
    app = create_app()
    
    with app.app_context():
        # Limpar dados existentes (opcional)
        print("🗑️  Limpando dados antigos...")
        db.drop_all()
        db.create_all()
        
        print("📊 Criando sanções de exemplo...")
        
        # Sanções
        sancoes = [
            Sancao(
                cpf_cnpj="12345678000190",
                nome_sancionado="Empresa Teste LTDA",
                tipo_pessoa="PJ",
                tipo_sancao="Suspensão Temporária",
                orgao_sancionador="CGU - Controladoria Geral da União",
                data_inicio_sancao=date(2023, 1, 1),
                data_fim_sancao=date(2025, 12, 31),
                motivo="Fraude em licitação pública",
                fonte="CEIS"
            ),
            Sancao(
                cpf_cnpj="98765432000100",
                nome_sancionado="Construtora ABC S/A",
                tipo_pessoa="PJ",
                tipo_sancao="Declaração de Inidoneidade",
                orgao_sancionador="TCU - Tribunal de Contas da União",
                data_inicio_sancao=date(2022, 6, 15),
                data_fim_sancao=date(2024, 6, 15),
                motivo="Superfaturamento em obras públicas",
                fonte="CEIS"
            ),
            Sancao(
                cpf_cnpj="11122233000145",
                nome_sancionado="Serviços XYZ LTDA",
                tipo_pessoa="PJ",
                tipo_sancao="Impedimento de Licitar",
                orgao_sancionador="Ministério da Saúde",
                data_inicio_sancao=date(2023, 3, 1),
                data_fim_sancao=date(2026, 3, 1),
                motivo="Inexecução contratual",
                fonte="CEPIM"
            ),
            Sancao(
                cpf_cnpj="12345678901",
                nome_sancionado="João Silva Santos",
                tipo_pessoa="PF",
                tipo_sancao="Impedimento de Licitar",
                orgao_sancionador="Prefeitura Municipal",
                data_inicio_sancao=date(2023, 5, 10),
                data_fim_sancao=date(2025, 5, 10),
                motivo="Conflito de interesses",
                fonte="CEIS"
            )
        ]
        
        for sancao in sancoes:
            db.session.add(sancao)
        
        print("📄 Criando contratos de exemplo...")
        
        # Contratos
        contratos = [
            Contrato(
                numero_contrato="2023/001-MS",
                cpf_cnpj_contratado="12345678000190",
                nome_contratado="Empresa Teste LTDA",
                orgao_contratante="Ministério da Saúde",
                objeto="Prestação de serviços médicos hospitalares",
                valor=Decimal("500000.00"),
                data_assinatura=date(2023, 6, 15),
                data_inicio_vigencia=date(2023, 7, 1),
                data_fim_vigencia=date(2024, 6, 30),
                fonte="Portal da Transparência",
                url_fonte="https://portaldatransparencia.gov.br"
            ),
            Contrato(
                numero_contrato="2023/002-INCRA",
                cpf_cnpj_contratado="12345678000190",
                nome_contratado="Empresa Teste LTDA",
                orgao_contratante="INCRA - Instituto Nacional de Colonização",
                objeto="Consultoria técnica para regularização fundiária",
                valor=Decimal("300000.00"),
                data_assinatura=date(2023, 8, 20),
                data_inicio_vigencia=date(2023, 9, 1),
                data_fim_vigencia=date(2024, 2, 28),
                fonte="Portal da Transparência",
                url_fonte="https://portaldatransparencia.gov.br"
            ),
            Contrato(
                numero_contrato="2023/010-DNIT",
                cpf_cnpj_contratado="98765432000100",
                nome_contratado="Construtora ABC S/A",
                orgao_contratante="DNIT - Departamento Nacional de Infraestrutura",
                objeto="Construção e pavimentação de rodovia BR-XXX",
                valor=Decimal("2000000.00"),
                data_assinatura=date(2023, 2, 10),
                data_inicio_vigencia=date(2023, 3, 1),
                data_fim_vigencia=date(2025, 12, 31),
                fonte="Portal da Transparência",
                url_fonte="https://portaldatransparencia.gov.br"
            ),
            Contrato(
                numero_contrato="2024/005-FUNAI",
                cpf_cnpj_contratado="11122233000145",
                nome_contratado="Serviços XYZ LTDA",
                orgao_contratante="FUNAI - Fundação Nacional do Índio",
                objeto="Levantamento topográfico em terras indígenas",
                valor=Decimal("150000.00"),
                data_assinatura=date(2024, 1, 30),
                data_inicio_vigencia=date(2024, 2, 15),
                data_fim_vigencia=date(2024, 8, 15),
                fonte="Portal da Transparência",
                url_fonte="https://portaldatransparencia.gov.br"
            ),
            Contrato(
                numero_contrato="2023/050-MEC",
                cpf_cnpj_contratado="99988877000166",
                nome_contratado="Educação Tech LTDA",
                orgao_contratante="Ministério da Educação",
                objeto="Fornecimento de equipamentos de informática",
                valor=Decimal("750000.00"),
                data_assinatura=date(2023, 4, 5),
                data_inicio_vigencia=date(2023, 5, 1),
                data_fim_vigencia=date(2023, 12, 31),
                fonte="PNCP",
                url_fonte="https://pncp.gov.br"
            )
        ]
        
        for contrato in contratos:
            db.session.add(contrato)
        
        print("⚠️  Criando alertas de integridade...")
        
        # Alertas
        alertas = [
            AlertaIntegridade(
                cpf_cnpj="12345678000190",
                nome="Empresa Teste LTDA",
                tipo_alerta="contrato_durante_sancao",
                nivel_risco=RISK_LEVEL.critico,
                descricao="Empresa sancionada firmou 2 contratos durante período de suspensão ativa",
                dados_json={
                    "contratos": ["2023/001-MS", "2023/002-INCRA"],
                    "valor_total": 800000.00,
                    "orgaos": ["Ministério da Saúde", "INCRA"]
                }
            ),
            AlertaIntegridade(
                cpf_cnpj="98765432000100",
                nome="Construtora ABC S/A",
                tipo_alerta="contrato_durante_sancao",
                nivel_risco=RISK_LEVEL.critico,
                descricao="Empresa com declaração de inidoneidade firmou contrato de R$ 2 milhões",
                dados_json={
                    "contratos": ["2023/010-DNIT"],
                    "valor_total": 2000000.00,
                    "orgaos": ["DNIT"]
                }
            ),
            AlertaIntegridade(
                cpf_cnpj="11122233000145",
                nome="Serviços XYZ LTDA",
                tipo_alerta="contrato_durante_sancao",
                nivel_risco=RISK_LEVEL.alto,
                descricao="Empresa impedida de licitar firmou contrato federal",
                dados_json={
                    "contratos": ["2024/005-FUNAI"],
                    "valor_total": 150000.00,
                    "orgaos": ["FUNAI"]
                }
            )
        ]
        
        for alerta in alertas:
            db.session.add(alerta)
        
        print("👤 Criando perfis de políticos...")
        
        # Políticos
        politicos = [
            PoliticoProfile(
                cpf="12345678901",
                nome="João Silva Santos",
                nome_urna="DR. JOÃO SILVA",
                partido="PXX",
                cargo="Deputado Federal",
                uf="SP",
                ano_eleicao=2022,
                situacao="Eleito",
                bens_declarados=[
                    {"ano": 2022, "tipo": "Imóvel", "valor": 500000.00},
                    {"ano": 2022, "tipo": "Veículo", "valor": 80000.00},
                    {"ano": 2022, "tipo": "Aplicações", "valor": 200000.00}
                ],
                total_bens_valor=Decimal("780000.00"),
                doacoes_recebidas=[
                    {"origem": "Pessoa Física", "valor": 50000.00},
                    {"origem": "Partido", "valor": 100000.00}
                ],
                total_doacoes=Decimal("150000.00"),
                empresas_vinculadas=[
                    {"cnpj": "12345678000190", "nome": "Empresa Teste LTDA", "qualificacao": "Sócio"}
                ],
                fonte_tse="Divulga Candidaturas 2022"
            ),
            PoliticoProfile(
                cpf="98765432100",
                nome="Maria Oliveira Santos",
                nome_urna="MARIA OLIVEIRA",
                partido="PYY",
                cargo="Senadora",
                uf="RJ",
                ano_eleicao=2022,
                situacao="Eleito",
                bens_declarados=[
                    {"ano": 2022, "tipo": "Imóvel", "valor": 1200000.00},
                    {"ano": 2022, "tipo": "Participação Societária", "valor": 500000.00}
                ],
                total_bens_valor=Decimal("1700000.00"),
                doacoes_recebidas=[
                    {"origem": "Pessoa Física", "valor": 200000.00},
                    {"origem": "Partido", "valor": 300000.00}
                ],
                total_doacoes=Decimal("500000.00"),
                empresas_vinculadas=[],
                fonte_tse="Divulga Candidaturas 2022"
            )
        ]
        
        for politico in politicos:
            db.session.add(politico)
        
        # Commit de tudo
        print("💾 Salvando no banco de dados...")
        db.session.commit()
        
        print("\n✅ Dados criados com sucesso!")
        print(f"   - {len(sancoes)} sanções")
        print(f"   - {len(contratos)} contratos")
        print(f"   - {len(alertas)} alertas")
        print(f"   - {len(politicos)} políticos")
        print("\n🎉 Banco de dados populado! Acesse http://localhost:5000")


if __name__ == "__main__":
    criar_dados_exemplo()
