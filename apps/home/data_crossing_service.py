"""
Serviço de cruzamento de dados para detectar irregularidades
"""
from __future__ import annotations

import csv
from datetime import datetime, date
from pathlib import Path
from typing import Any, List, Dict
import os

from apps.home.api_services import only_digits


def parse_date(date_str: str) -> date | None:
    """Converte string de data para objeto date"""
    if not date_str:
        return None
    
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def load_ceis_csv(path: str | Path) -> List[Dict[str, Any]]:
    """
    Carrega dados do CEIS de arquivo CSV
    """
    path = Path(path)
    if not path.exists():
        return []
    
    registros = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            registros.append({
                "cpf_cnpj": only_digits(row.get("cnpj_cpf", "")),
                "nome": row.get("name", ""),
                "data_inicio": parse_date(row.get("sanction_start", "")),
                "data_fim": parse_date(row.get("sanction_end", "")),
                "tipo_sancao": row.get("sanction_type", ""),
                "orgao": row.get("orgao_sancionador", ""),
            })
    
    return registros


def load_contratos_csv(path: str | Path) -> List[Dict[str, Any]]:
    """
    Carrega dados de contratos de arquivo CSV
    """
    path = Path(path)
    if not path.exists():
        return []
    
    registros = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            registros.append({
                "cpf_cnpj": only_digits(row.get("cpf_cnpj", "")),
                "nome": row.get("nome", ""),
                "numero_contrato": row.get("numero", ""),
                "orgao": row.get("orgao", ""),
                "valor": float(row.get("valor", 0) or 0),
                "data_assinatura": parse_date(row.get("data_assinatura", "")),
                "objeto": row.get("objeto", ""),
            })
    
    return registros


def verificar_sobreposicao_datas(
    data_contrato: date,
    data_inicio_sancao: date | None,
    data_fim_sancao: date | None
) -> bool:
    """
    Verifica se a data do contrato está dentro do período de sanção
    """
    if not data_contrato:
        return False
    
    if not data_inicio_sancao:
        return False
    
    # Se começou depois da sanção começar
    if data_contrato < data_inicio_sancao:
        return False
    
    # Se não tem data fim, considera sanção ativa
    if not data_fim_sancao:
        return True
    
    # Se contrato foi assinado antes do fim da sanção
    return data_contrato <= data_fim_sancao


def cruzar_sancoes_contratos(
    sancoes: List[Dict[str, Any]],
    contratos: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Cruza dados de sanções com contratos para identificar irregularidades
    
    Retorna lista de contratos firmados durante período de sanção ativa
    """
    irregularidades = []
    
    # Indexar sanções por CPF/CNPJ para busca rápida
    index_sancoes = {}
    for sancao in sancoes:
        doc = sancao["cpf_cnpj"]
        if doc not in index_sancoes:
            index_sancoes[doc] = []
        index_sancoes[doc].append(sancao)
    
    # Verificar cada contrato
    for contrato in contratos:
        doc = contrato["cpf_cnpj"]
        
        # Buscar sanções deste documento
        sancoes_doc = index_sancoes.get(doc, [])
        
        for sancao in sancoes_doc:
            # Verificar se contrato foi firmado durante sanção
            if verificar_sobreposicao_datas(
                contrato.get("data_assinatura"),
                sancao.get("data_inicio"),
                sancao.get("data_fim")
            ):
                irregularidades.append({
                    "cpf_cnpj": doc,
                    "nome": contrato.get("nome"),
                    "numero_contrato": contrato.get("numero_contrato"),
                    "orgao_contratante": contrato.get("orgao"),
                    "valor_contrato": contrato.get("valor", 0),
                    "data_contrato": contrato.get("data_assinatura"),
                    "tipo_sancao": sancao.get("tipo_sancao"),
                    "orgao_sancionador": sancao.get("orgao"),
                    "data_inicio_sancao": sancao.get("data_inicio"),
                    "data_fim_sancao": sancao.get("data_fim"),
                    "status": "CONTRATO DURANTE SANÇÃO ATIVA",
                    "nivel_risco": "CRÍTICO"
                })
    
    return irregularidades


def analisar_dados_locais() -> Dict[str, Any]:
    """
    Analisa dados de CEIS e contratos locais e retorna estatísticas
    """
    # Caminhos dos arquivos
    base_dir = Path(__file__).resolve().parents[2]
    ceis_path = base_dir / "old" / "data" / "raw" / "ceis.csv"
    contratos_path = base_dir / "old" / "data" / "raw" / "contracts.csv"
    
    # Carregar dados
    sancoes = load_ceis_csv(ceis_path)
    contratos = load_contratos_csv(contratos_path)
    
    # Cruzar dados
    irregularidades = cruzar_sancoes_contratos(sancoes, contratos)
    
    # Calcular estatísticas
    valor_total_contratos = sum(c.get("valor", 0) for c in contratos)
    valor_irregular = sum(i.get("valor_contrato", 0) for i in irregularidades)
    
    # Agrupar por empresa
    empresas_irregulares = {}
    for irreg in irregularidades:
        doc = irreg["cpf_cnpj"]
        if doc not in empresas_irregulares:
            empresas_irregulares[doc] = {
                "nome": irreg["nome"],
                "cpf_cnpj": doc,
                "contratos": [],
                "valor_total": 0
            }
        empresas_irregulares[doc]["contratos"].append(irreg)
        empresas_irregulares[doc]["valor_total"] += irreg.get("valor_contrato", 0)
    
    return {
        "total_sancoes": len(sancoes),
        "total_contratos": len(contratos),
        "total_irregularidades": len(irregularidades),
        "valor_total_contratos": valor_total_contratos,
        "valor_irregular": valor_irregular,
        "percentual_irregular": (valor_irregular / valor_total_contratos * 100) if valor_total_contratos > 0 else 0,
        "empresas_irregulares": list(empresas_irregulares.values()),
        "irregularidades": irregularidades,
        "arquivos_analisados": {
            "ceis": str(ceis_path),
            "contratos": str(contratos_path)
        }
    }


def buscar_vinculos_politicos(cpf_politico: str, dados_qsa: List[Dict]) -> List[Dict[str, Any]]:
    """
    Busca vínculos de um político em empresas através do QSA (Quadro de Sócios e Administradores)
    """
    cpf = only_digits(cpf_politico)
    vinculos = []
    
    for registro in dados_qsa:
        cpf_socio = only_digits(registro.get("cpf", ""))
        if cpf_socio == cpf:
            vinculos.append({
                "nome_socio": registro.get("nome", ""),
                "cpf": cpf,
                "qualificacao": registro.get("qual", ""),
                "cnpj_empresa": registro.get("cnpj_empresa", ""),
                "nome_empresa": registro.get("nome_empresa", "")
            })
    
    return vinculos


def detectar_padroes_suspeitos(dados: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detecta padrões suspeitos nos dados analisados
    """
    padroes = []
    
    # Padrão 1: Empresa com múltiplos contratos durante sanção
    empresas_irreg = dados.get("empresas_irregulares", [])
    for emp in empresas_irreg:
        if len(emp["contratos"]) > 1:
            padroes.append({
                "tipo": "MULTIPLOS_CONTRATOS_DURANTE_SANCAO",
                "gravidade": "CRÍTICA",
                "descricao": f"{emp['nome']} firmou {len(emp['contratos'])} contratos durante sanção ativa",
                "entidade": emp["nome"],
                "cpf_cnpj": emp["cpf_cnpj"],
                "detalhes": emp
            })
    
    # Padrão 2: Contratos de alto valor durante sanção
    for emp in empresas_irreg:
        if emp["valor_total"] > 1000000:  # Mais de 1 milhão
            padroes.append({
                "tipo": "ALTO_VALOR_DURANTE_SANCAO",
                "gravidade": "CRÍTICA",
                "descricao": f"{emp['nome']} firmou contratos de R$ {emp['valor_total']:,.2f} durante sanção",
                "entidade": emp["nome"],
                "cpf_cnpj": emp["cpf_cnpj"],
                "valor": emp["valor_total"]
            })
    
    # Padrão 3: Taxa de irregularidade alta
    perc_irreg = dados.get("percentual_irregular", 0)
    if perc_irreg > 5:
        padroes.append({
            "tipo": "ALTA_TAXA_IRREGULARIDADE",
            "gravidade": "ALTA",
            "descricao": f"{perc_irreg:.2f}% do valor total de contratos está irregular",
            "percentual": perc_irreg
        })
    
    return padroes
