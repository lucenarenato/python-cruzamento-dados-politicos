from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd


def _clean_document(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = str(value)
    return "".join(ch for ch in text if ch.isdigit())


def _to_date(value: Any) -> date | None:
    if pd.isna(value) or value in ("", None):
        return None
    converted = pd.to_datetime(value, errors="coerce", dayfirst=True)
    if pd.isna(converted):
        return None
    return converted.date()


@dataclass(frozen=True)
class SanctionRecord:
    source_id: str
    cnpj_cpf: str
    name: str
    sanction_start: date | None
    sanction_end: date | None
    sanction_type: str


@dataclass(frozen=True)
class ContractRecord:
    source_id: str
    supplier_document: str
    supplier_name: str
    contract_date: date | None
    contract_value: float | None
    contract_number: str
    organ: str


def parse_sanction_row(row: pd.Series) -> SanctionRecord:
    return SanctionRecord(
        source_id=str(row.get("source_id", "")).strip(),
        cnpj_cpf=_clean_document(row.get("cnpj_cpf", "")),
        name=str(row.get("name", "")).strip(),
        sanction_start=_to_date(row.get("sanction_start")),
        sanction_end=_to_date(row.get("sanction_end")),
        sanction_type=str(row.get("sanction_type", "")).strip(),
    )


def parse_contract_row(row: pd.Series) -> ContractRecord:
    value = row.get("contract_value")
    contract_value: float | None
    if pd.isna(value):
        contract_value = None
    else:
        try:
            contract_value = float(value)
        except (ValueError, TypeError):
            contract_value = None

    return ContractRecord(
        source_id=str(row.get("source_id", "")).strip(),
        supplier_document=_clean_document(row.get("supplier_document", "")),
        supplier_name=str(row.get("supplier_name", "")).strip(),
        contract_date=_to_date(row.get("contract_date")),
        contract_value=contract_value,
        contract_number=str(row.get("contract_number", "")).strip(),
        organ=str(row.get("organ", "")).strip(),
    )