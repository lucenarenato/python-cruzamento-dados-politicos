from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    ceis_csv: Path
    contracts_csv: Path
    output_dir: Path


def _path_from_env(key: str, fallback: str) -> Path:
    return Path(os.getenv(key, fallback)).expanduser().resolve()


def load_settings() -> Settings:
    data_dir = _path_from_env("DATA_DIR", "./data")
    return Settings(
        data_dir=data_dir,
        ceis_csv=_path_from_env("CEIS_CSV", str(data_dir / "raw/ceis.csv")),
        contracts_csv=_path_from_env("CONTRACTS_CSV", str(data_dir / "raw/contracts.csv")),
        output_dir=_path_from_env("OUTPUT_DIR", "./data/output"),
    )