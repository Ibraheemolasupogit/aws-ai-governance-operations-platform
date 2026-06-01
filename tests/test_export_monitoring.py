import json

import pandas as pd

from ai_governance_platform.monitoring.export_monitoring import (
    export_monitoring,
    export_monitoring_to_csv,
    export_monitoring_to_json,
)
from ai_governance_platform.monitoring.generate_monitoring import (
    generate_sample_monitoring_records,
)


def test_export_monitoring_to_csv_creates_file(tmp_path) -> None:
    records = generate_sample_monitoring_records()
    output_path = tmp_path / "model_monitoring.csv"

    created_path = export_monitoring_to_csv(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(records)
    assert "health_status" in exported.columns


def test_export_monitoring_to_json_creates_file(tmp_path) -> None:
    records = generate_sample_monitoring_records()
    output_path = tmp_path / "model_monitoring.json"

    created_path = export_monitoring_to_json(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(records)
    assert "health_status" in exported[0]


def test_export_monitoring_creates_csv_and_json(tmp_path) -> None:
    records = generate_sample_monitoring_records()
    csv_path = tmp_path / "model_monitoring.csv"
    json_path = tmp_path / "model_monitoring.json"

    created_csv_path, created_json_path = export_monitoring(records, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
