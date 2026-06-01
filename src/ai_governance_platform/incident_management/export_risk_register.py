"""Export AI risk register records."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.incident_management.risk_register_schema import RiskRegisterRecord

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "model_risk_register.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "model_risk_register.json"


def _records_to_dicts(records: Iterable[RiskRegisterRecord]) -> list[dict]:
    return [record.model_dump(mode="json") for record in records]


def export_risk_register_to_csv(
    records: Iterable[RiskRegisterRecord], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_records_to_dicts(records)).to_csv(path, index=False)
    return path


def export_risk_register_to_json(
    records: Iterable[RiskRegisterRecord], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_records_to_dicts(records), indent=2), encoding="utf-8")
    return path


def export_risk_register(
    records: Iterable[RiskRegisterRecord],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    record_list = list(records)
    return (
        export_risk_register_to_csv(record_list, csv_path),
        export_risk_register_to_json(record_list, json_path),
    )
