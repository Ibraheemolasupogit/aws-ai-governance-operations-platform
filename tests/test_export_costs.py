import json

import pandas as pd

from ai_governance_platform.cost_management.export_costs import (
    export_costs,
    export_costs_to_csv,
    export_costs_to_json,
)
from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records


def test_export_costs_to_csv_creates_file(tmp_path) -> None:
    records = generate_sample_cost_records()
    output_path = tmp_path / "cost_monitoring.csv"

    created_path = export_costs_to_csv(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(records)
    assert "estimated_total_cost" in exported.columns


def test_export_costs_to_json_creates_file(tmp_path) -> None:
    records = generate_sample_cost_records()
    output_path = tmp_path / "cost_monitoring.json"

    created_path = export_costs_to_json(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(records)
    assert "estimated_total_cost" in exported[0]


def test_export_costs_creates_csv_and_json(tmp_path) -> None:
    records = generate_sample_cost_records()
    csv_path = tmp_path / "cost_monitoring.csv"
    json_path = tmp_path / "cost_monitoring.json"

    created_csv_path, created_json_path = export_costs(records, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
