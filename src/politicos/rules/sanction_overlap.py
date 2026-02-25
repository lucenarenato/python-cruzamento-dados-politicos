from __future__ import annotations

import pandas as pd


def _digits_only(value: object) -> str:
    if pd.isna(value):
        return ""
    return "".join(ch for ch in str(value) if ch.isdigit())


def find_contracts_during_sanction(
    sanctions: pd.DataFrame,
    contracts: pd.DataFrame,
) -> pd.DataFrame:
    sanctions = sanctions.copy()
    contracts = contracts.copy()

    sanctions["doc_key"] = sanctions["cnpj_cpf"].map(_digits_only)
    contracts["doc_key"] = contracts["supplier_document"].map(_digits_only)

    sanctions["sanction_start"] = pd.to_datetime(
        sanctions["sanction_start"], errors="coerce", dayfirst=True
    )
    sanctions["sanction_end"] = pd.to_datetime(
        sanctions["sanction_end"], errors="coerce", dayfirst=True
    )
    contracts["contract_date"] = pd.to_datetime(
        contracts["contract_date"], errors="coerce", dayfirst=True
    )

    sanctions = sanctions[sanctions["doc_key"] != ""]
    contracts = contracts[contracts["doc_key"] != ""]
    contracts = contracts[contracts["contract_date"].notna()]
    sanctions = sanctions[sanctions["sanction_start"].notna()]

    merged = contracts.merge(
        sanctions,
        on="doc_key",
        suffixes=("_contract", "_sanction"),
        how="inner",
    )

    end_date = merged["sanction_end"].fillna(pd.Timestamp.max)
    in_window = (merged["contract_date"] >= merged["sanction_start"]) & (
        merged["contract_date"] <= end_date
    )

    flagged = merged[in_window].copy()

    ordered = [
        "doc_key",
        "supplier_name",
        "contract_number",
        "contract_date",
        "contract_value",
        "organ",
        "name",
        "sanction_type",
        "sanction_start",
        "sanction_end",
    ]
    existing = [col for col in ordered if col in flagged.columns]
    if existing:
        flagged = flagged[existing]

    flagged = flagged.sort_values(by=["contract_date", "doc_key"]).reset_index(drop=True)
    return flagged