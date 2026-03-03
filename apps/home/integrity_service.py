from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TRANSPARENCIA_BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def consultar_portal_transparencia(documento: str) -> dict[str, Any]:
    doc = only_digits(documento)
    if len(doc) not in (11, 14):
        return {
            "ok": False,
            "erro": "Informe um CPF/CNPJ válido contendo 11 ou 14 dígitos.",
        }

    api_key = os.getenv("TRANSPARENCIA_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "erro": "Defina TRANSPARENCIA_API_KEY no ambiente para consultar o Portal da Transparência.",
        }

    query = urlencode({"codigo": doc})
    url = f"{TRANSPARENCIA_BASE_URL}/pesquisa-binaria?{query}"
    request = Request(url, headers={"chave-api-dados": api_key})

    try:
        with urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body) if body else []

        return {
            "ok": True,
            "documento": doc,
            "fonte": "Portal da Transparência",
            "endpoint": "/pesquisa-binaria",
            "total_registros": len(data) if isinstance(data, list) else 1,
            "dados": data,
        }
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        print(f"[DEBUG] HTTPError {exc.code}: {details}")
        return {
            "ok": False,
            "erro": f"Erro HTTP {exc.code} ao consultar API.",
            "detalhes": details,
        }
    except URLError as exc:
        print(f"[DEBUG] URLError: {exc.reason}")
        return {
            "ok": False,
            "erro": f"Falha de conexão com a API: {exc.reason}",
        }
    except json.JSONDecodeError:
        print(f"[DEBUG] JSONDecodeError: Resposta não é JSON válido")
        return {
            "ok": False,
            "erro": "A API retornou conteúdo inválido (não JSON).",
        }


def _default_ceis_csv_path() -> Path:
    # Navega até a raiz do projeto: integrity_service.py -> home -> apps -> projeto_root
    return Path(__file__).resolve().parents[2] / "data" / "raw" / "ceis.csv"


def consultar_ceis_local(documento: str) -> dict[str, Any]:
    doc = only_digits(documento)
    if len(doc) not in (11, 14):
        return {
            "ok": False,
            "erro": "Informe um CPF/CNPJ válido contendo 11 ou 14 dígitos.",
        }

    ceis_path = Path(os.getenv("CEIS_CSV", str(_default_ceis_csv_path())))
    if not ceis_path.exists():
        return {
            "ok": False,
            "erro": f"Arquivo CEIS não encontrado em: {ceis_path}",
        }

    try:
        matches: list[dict[str, Any]] = []
        with ceis_path.open("r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                row_doc = only_digits(row.get("cnpj_cpf", ""))
                if row_doc == doc:
                    matches.append(
                        {
                            "source_id": row.get("source_id", "CEIS"),
                            "cnpj_cpf": row.get("cnpj_cpf", ""),
                            "name": row.get("name", ""),
                            "sanction_start": row.get("sanction_start", ""),
                            "sanction_end": row.get("sanction_end", ""),
                            "sanction_type": row.get("sanction_type", ""),
                        }
                    )

        return {
            "ok": True,
            "documento": doc,
            "fonte": "CEIS (arquivo local)",
            "arquivo": str(ceis_path),
            "total_registros": len(matches),
            "dados": matches,
        }
    except Exception as exc:
        return {
            "ok": False,
            "erro": f"Falha ao ler CEIS local: {exc}",
        }


def analisar_integridade(documento: str) -> dict[str, Any]:
    doc = only_digits(documento)
    portal = consultar_portal_transparencia(doc)
    ceis = consultar_ceis_local(doc)

    ceis_hits = ceis.get("total_registros", 0) if ceis.get("ok") else 0
    portal_hits = portal.get("total_registros", 0) if portal.get("ok") else 0

    nivel = "baixo"
    motivos: list[str] = []

    if ceis_hits > 0:
        nivel = "alto"
        motivos.append("Documento encontrado em base de sanções CEIS.")
    elif portal_hits > 0:
        nivel = "medio"
        motivos.append("Há registros no Portal da Transparência para o documento.")
    else:
        motivos.append("Nenhum registro encontrado nas fontes consultadas.")

    return {
        "documento": doc,
        "portal": portal,
        "ceis": ceis,
        "resumo": {
            "nivel_risco": nivel,
            "motivos": motivos,
            "fontes_consultadas": 2,
            "total_registros": ceis_hits + portal_hits,
        },
    }
