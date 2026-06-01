"""Export AI platform cost monitoring records."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.cost_management.schema import CostRecord

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "cost_monitoring.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "cost_monitoring.json"


def _records_to_dicts(records: Iterable[CostRecord]) -> list[dict]:
    return [record.model_dump(mode="json") for record in records]


def export_costs_to_csv(
    records: Iterable[CostRecord], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_records_to_dicts(records)).to_csv(path, index=False)
    return path


def export_costs_to_json(
    records: Iterable[CostRecord], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_records_to_dicts(records), indent=2), encoding="utf-8")
    return path


def export_costs(
    records: Iterable[CostRecord],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    record_list = list(records)
    return export_costs_to_csv(record_list, csv_path), export_costs_to_json(record_list, json_path)
