from __future__ import annotations

import argparse
import json
from pathlib import Path

from politicos.config import load_settings
from politicos.pipeline import run_sanctions_vs_contracts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="politicos",
        description="Pipeline de análise de risco em contratos públicos",
    )
    parser.add_argument(
        "command",
        choices=["scan-sanctions"],
        help="Comando a executar",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Diretório de saída para arquivos gerados",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    settings = load_settings()
    if args.output_dir is not None:
        settings = settings.__class__(
            data_dir=settings.data_dir,
            ceis_csv=settings.ceis_csv,
            contracts_csv=settings.contracts_csv,
            output_dir=args.output_dir.resolve(),
        )

    if args.command == "scan-sanctions":
        summary = run_sanctions_vs_contracts(settings)
        print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()