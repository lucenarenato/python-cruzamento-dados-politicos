from __future__ import annotations

from pathlib import Path

import pandas as pd

from politicos.connectors.csv_loader import load_csv, normalize_columns, require_columns


def load_ceis(path: Path) -> pd.DataFrame:
    df = load_csv(path)
    df = normalize_columns(df)

    aliases = {
        "cpf_cnpj": "cnpj_cpf",
        "documento": "cnpj_cpf",
        "razao_social": "name",
        "nome_sancionado": "name",
        "data_inicio_sancao": "sanction_start",
        "data_fim_sancao": "sanction_end",
        "tipo_sancao": "sanction_type",
    }
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns})

    required = ["cnpj_cpf", "name", "sanction_start"]
    require_columns(df, required, "CEIS")

    if "source_id" not in df.columns:
        df["source_id"] = "CEIS"
    if "sanction_end" not in df.columns:
        df["sanction_end"] = pd.NA
    if "sanction_type" not in df.columns:
        df["sanction_type"] = ""

    return df[
        ["source_id", "cnpj_cpf", "name", "sanction_start", "sanction_end", "sanction_type"]
    ]