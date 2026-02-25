from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            "Arquivo não encontrado: "
            f"{path}. "
            "Crie os CSVs em data/raw ou rode `make init-data` para gerar exemplos."
        )
    return pd.read_csv(path)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    return df.rename(columns=renamed)


def require_columns(df: pd.DataFrame, required: list[str], context: str) -> None:
    missing = [name for name in required if name not in df.columns]
    if missing:
        raise ValueError(
            f"{context}: colunas obrigatórias ausentes: {', '.join(missing)}"
        )