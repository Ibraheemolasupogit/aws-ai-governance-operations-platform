"""Export local AI system inventory records."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.inventory.schema import AISystemRecord

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "ai_system_inventory.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "ai_system_inventory.json"


def _records_to_dicts(records: Iterable[AISystemRecord]) -> list[dict]:
    return [record.model_dump(mode="json") for record in records]


def export_inventory_to_csv(
    records: Iterable[AISystemRecord], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    """Export inventory records to CSV and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_records_to_dicts(records)).to_csv(path, index=False)
    return path


def export_inventory_to_json(
    records: Iterable[AISystemRecord], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    """Export inventory records to JSON and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_records_to_dicts(records), indent=2), encoding="utf-8")
    return path


def export_inventory(
    records: Iterable[AISystemRecord],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    """Export inventory records to CSV and JSON."""
    record_list = list(records)
    return (
        export_inventory_to_csv(record_list, csv_path),
        export_inventory_to_json(record_list, json_path),
    )
