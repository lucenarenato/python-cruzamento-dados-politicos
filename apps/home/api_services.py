"""
Serviços para consulta em APIs públicas do governo federal
"""
from __future__ import annotations

import json
import os
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from datetime import datetime, timedelta


def only_digits(value: str) -> str:
    """Remove tudo exceto dígitos"""
    return re.sub(r"\D", "", value or "")


def format_cpf_cnpj(doc: str) -> str:
    """Formata CPF ou CNPJ"""
    doc = only_digits(doc)
    if len(doc) == 11:
        return f"{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}"
    elif len(doc) == 14:
        return f"{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}"
    return doc


class PortalTransparenciaAPI:
    """Cliente para API do Portal da Transparência"""
    
    BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
    
    def __init__(self):
        self.api_key = os.getenv("TRANSPARENCIA_API_KEY", "")
    
    def _request(self, endpoint: str, params: dict = None) -> dict[str, Any]:
        """Faz requisição à API"""
        if not self.api_key:
            return {
                "ok": False,
                "erro": "TRANSPARENCIA_API_KEY não configurada"
            }
        
        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            url += f"?{urlencode(params)}"
        
        request = Request(url, headers={"chave-api-dados": self.api_key})
        
        try:
            with urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body) if body else []
            
            return {
                "ok": True,
                "dados": data,
                "total": len(data) if isinstance(data, list) else 1
            }
        except HTTPError as exc:
            return {
                "ok": False,
                "erro": f"HTTP {exc.code}",
                "detalhes": exc.read().decode("utf-8", errors="ignore")
            }
        except URLError as exc:
            return {
                "ok": False,
                "erro": f"Erro de conexão: {exc.reason}"
            }
        except Exception as exc:
            return {
                "ok": False,
                "erro": str(exc)
            }
    
    def buscar_ceis(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca empresas/pessoas sancionadas no CEIS"""
        doc = only_digits(cpf_cnpj)
        return self._request(f"ceis", {"codigoSancionado": doc})
    
    def buscar_cnep(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca no Cadastro Nacional de Empresas Punidas"""
        doc = only_digits(cpf_cnpj)
        return self._request(f"cnep", {"codigoSancionado": doc})
    
    def buscar_cepim(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca impedidos de licitar - CEPIM"""
        doc = only_digits(cpf_cnpj)
        return self._request(f"cepim", {"codigoSancionado": doc})
    
    def buscar_contratos(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca contratos por CNPJ/CPF"""
        doc = only_digits(cpf_cnpj)
        return self._request(f"contratos", {"cnpjContratado": doc})
    
    def buscar_convenios(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca convênios por CNPJ/CPF"""
        doc = only_digits(cpf_cnpj)
        return self._request(f"convenios", {"cnpjConvenente": doc})


class ReceitaFederalAPI:
    """Cliente para consultas na Receita Federal (CNPJ)"""
    
    # API pública não oficial - ReceitaWS
    BASE_URL = "https://www.receitaws.com.br/v1"
    
    def consultar_cnpj(self, cnpj: str) -> dict[str, Any]:
        """Consulta dados de CNPJ"""
        doc = only_digits(cnpj)
        if len(doc) != 14:
            return {
                "ok": False,
                "erro": "CNPJ deve ter 14 dígitos"
            }
        
        url = f"{self.BASE_URL}/cnpj/{doc}"
        request = Request(url)
        
        try:
            with urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body)
            
            if data.get("status") == "ERROR":
                return {
                    "ok": False,
                    "erro": data.get("message", "Erro ao consultar CNPJ")
                }
            
            return {
                "ok": True,
                "dados": data,
                "qsa": data.get("qsa", [])  # Quadro de Sócios e Administradores
            }
        except Exception as exc:
            return {
                "ok": False,
                "erro": str(exc)
            }


class PNCPAPI:
    """Cliente para Portal Nacional de Contratações Públicas"""
    
    BASE_URL = "https://pncp.gov.br/api"
    
    def buscar_contratos(self, cnpj: str, dias: int = 365) -> dict[str, Any]:
        """Busca contratos no PNCP"""
        doc = only_digits(cnpj)
        if len(doc) != 14:
            return {
                "ok": False,
                "erro": "CNPJ deve ter 14 dígitos"
            }
        
        # Data de início da busca
        data_inicio = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        
        params = {
            "cnpjContratada": doc,
            "dataInicial": data_inicio
        }
        
        url = f"{self.BASE_URL}/consulta/v1/contratos?{urlencode(params)}"
        request = Request(url)
        
        try:
            with urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body)
            
            return {
                "ok": True,
                "dados": data.get("data", []),
                "total": data.get("count", 0)
            }
        except HTTPError as exc:
            if exc.code == 404:
                return {
                    "ok": True,
                    "dados": [],
                    "total": 0,
                    "mensagem": "Nenhum contrato encontrado"
                }
            return {
                "ok": False,
                "erro": f"HTTP {exc.code}"
            }
        except Exception as exc:
            return {
                "ok": False,
                "erro": str(exc)
            }


class TSEAPI:
    """Cliente para dados eleitorais do TSE"""
    
    # O TSE disponibiliza dados via DivulgaCandContas, mas não tem API REST oficial
    # Aqui seria necessário parsear os arquivos CSV/JSON disponibilizados
    
    def buscar_candidaturas(self, cpf: str) -> dict[str, Any]:
        """Busca candidaturas de um CPF"""
        # Implementação simplificada - necessita download dos dados do TSE
        return {
            "ok": False,
            "erro": "Função requer download de base de dados do TSE",
            "info": "Acesse https://dadosabertos.tse.jus.br/"
        }
    
    def buscar_bens_declarados(self, cpf: str) -> dict[str, Any]:
        """Busca bens declarados por candidato"""
        return {
            "ok": False,
            "erro": "Função requer download de base de dados do TSE",
            "info": "Acesse https://dadosabertos.tse.jus.br/"
        }
    
    def buscar_doacoes(self, cpf_cnpj: str) -> dict[str, Any]:
        """Busca doações eleitorais"""
        return {
            "ok": False,
            "erro": "Função requer download de base de dados do TSE",
            "info": "Acesse https://dadosabertos.tse.jus.br/"
        }


def consultar_multiplas_fontes(cpf_cnpj: str) -> dict[str, Any]:
    """
    Consulta um CPF/CNPJ em múltiplas fontes de dados abertos
    """
    doc = only_digits(cpf_cnpj)
    tipo = "CPF" if len(doc) == 11 else "CNPJ" if len(doc) == 14 else "INVALIDO"
    
    if tipo == "INVALIDO":
        return {
            "ok": False,
            "erro": "Documento inválido. Informe CPF (11 dígitos) ou CNPJ (14 dígitos)"
        }
    
    resultado = {
        "documento": doc,
        "tipo": tipo,
        "documento_formatado": format_cpf_cnpj(doc),
        "timestamp": datetime.now().isoformat(),
        "fontes": {}
    }
    
    # Portal da Transparência
    pt_api = PortalTransparenciaAPI()
    
    resultado["fontes"]["ceis"] = pt_api.buscar_ceis(doc)
    resultado["fontes"]["cnep"] = pt_api.buscar_cnep(doc)
    resultado["fontes"]["cepim"] = pt_api.buscar_cepim(doc)
    resultado["fontes"]["contratos"] = pt_api.buscar_contratos(doc)
    resultado["fontes"]["convenios"] = pt_api.buscar_convenios(doc)
    
    # CNPJ específico
    if tipo == "CNPJ":
        rf_api = ReceitaFederalAPI()
        resultado["fontes"]["receita_federal"] = rf_api.consultar_cnpj(doc)
        
        pncp_api = PNCPAPI()
        resultado["fontes"]["pncp"] = pncp_api.buscar_contratos(doc)
    
    # TSE (CPF)
    if tipo == "CPF":
        tse_api = TSEAPI()
        resultado["fontes"]["tse_candidaturas"] = tse_api.buscar_candidaturas(doc)
        resultado["fontes"]["tse_bens"] = tse_api.buscar_bens_declarados(doc)
    
    return resultado


def calcular_nivel_risco(dados: dict[str, Any]) -> dict[str, Any]:
    """
    Calcula nível de risco baseado nos dados encontrados
    """
    pontos = 0
    alertas = []
    
    fontes = dados.get("fontes", {})
    
    # Sanções são muito graves
    if fontes.get("ceis", {}).get("ok") and fontes["ceis"].get("total", 0) > 0:
        pontos += 50
        alertas.append(f"Encontrado em CEIS ({fontes['ceis']['total']} registro(s))")
    
    if fontes.get("cnep", {}).get("ok") and fontes["cnep"].get("total", 0) > 0:
        pontos += 50
        alertas.append(f"Encontrado em CNEP ({fontes['cnep']['total']} registro(s))")
    
    if fontes.get("cepim", {}).get("ok") and fontes["cepim"].get("total", 0) > 0:
        pontos += 40
        alertas.append(f"Encontrado em CEPIM ({fontes['cepim']['total']} registro(s))")
    
    # Contratos e convênios são informativos
    if fontes.get("contratos", {}).get("ok") and fontes["contratos"].get("total", 0) > 0:
        num_contratos = fontes["contratos"]["total"]
        alertas.append(f"{num_contratos} contrato(s) federal(is)")
        if num_contratos > 10:
            pontos += 5
    
    if fontes.get("convenios", {}).get("ok") and fontes["convenios"].get("total", 0) > 0:
        num_convenios = fontes["convenios"]["total"]
        alertas.append(f"{num_convenios} convênio(s)")
    
    # Determinar nível
    if pontos >= 50:
        nivel = "critico"
    elif pontos >= 30:
        nivel = "alto"
    elif pontos >= 10:
        nivel = "medio"
    else:
        nivel = "baixo"
    
    return {
        "nivel_risco": nivel,
        "pontuacao": pontos,
        "alertas": alertas,
        "total_fontes_consultadas": len(fontes),
        "fontes_com_dados": sum(1 for f in fontes.values() if f.get("ok") and f.get("total", 0) > 0)
    }
