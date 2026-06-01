import json

import pandas as pd

from ai_governance_platform.audit.export_audit_events import (
    export_audit_events,
    export_audit_events_to_csv,
    export_audit_events_to_json,
)
from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events


def test_export_audit_events_to_csv_creates_file(tmp_path) -> None:
    events = generate_sample_audit_events()
    output_path = tmp_path / "audit_events.csv"

    created_path = export_audit_events_to_csv(events, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(events)
    assert "event_category" in exported.columns


def test_export_audit_events_to_json_creates_file(tmp_path) -> None:
    events = generate_sample_audit_events()
    output_path = tmp_path / "audit_events.json"

    created_path = export_audit_events_to_json(events, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(events)
    assert "event_category" in exported[0]


def test_export_audit_events_creates_csv_and_json(tmp_path) -> None:
    events = generate_sample_audit_events()
    csv_path = tmp_path / "audit_events.csv"
    json_path = tmp_path / "audit_events.json"

    created_csv_path, created_json_path = export_audit_events(events, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
