from __future__ import annotations

from pathlib import Path

import pandas as pd

from politicos.connectors.csv_loader import load_csv, normalize_columns, require_columns


def load_contracts(path: Path) -> pd.DataFrame:
    df = load_csv(path)
    df = normalize_columns(df)

    aliases = {
        "cnpj_cpf_fornecedor": "supplier_document",
        "documento_fornecedor": "supplier_document",
        "fornecedor_documento": "supplier_document",
        "fornecedor": "supplier_name",
        "nome_fornecedor": "supplier_name",
        "data_contrato": "contract_date",
        "valor_contrato": "contract_value",
        "numero_contrato": "contract_number",
        "orgao": "organ",
    }
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns})

    required = ["supplier_document", "supplier_name", "contract_date"]
    require_columns(df, required, "Contratos")

    if "source_id" not in df.columns:
        df["source_id"] = "CONTRACTS"
    if "contract_value" not in df.columns:
        df["contract_value"] = pd.NA
    if "contract_number" not in df.columns:
        df["contract_number"] = ""
    if "organ" not in df.columns:
        df["organ"] = ""

    return df[
        [
            "source_id",
            "supplier_document",
            "supplier_name",
            "contract_date",
            "contract_value",
            "contract_number",
            "organ",
        ]
    ]