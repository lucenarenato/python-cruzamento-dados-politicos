from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from politicos.connectors import load_ceis, load_contracts
from politicos.config import Settings
from politicos.rules import find_contracts_during_sanction


def run_sanctions_vs_contracts(settings: Settings) -> dict:
    sanctions = load_ceis(settings.ceis_csv)
    contracts = load_contracts(settings.contracts_csv)
    flagged = find_contracts_during_sanction(sanctions, contracts)

    settings.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = settings.output_dir / "contracts_during_sanction.csv"
    json_path = settings.output_dir / "summary.json"

    flagged.to_csv(csv_path, index=False)

    summary = {
        "sanctions_rows": int(len(sanctions)),
        "contracts_rows": int(len(contracts)),
        "flagged_rows": int(len(flagged)),
        "flagged_total_value": float(flagged["contract_value"].fillna(0).sum())
        if "contract_value" in flagged.columns
        else 0.0,
        "output_csv": str(csv_path),
    }

    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary