import json

import pandas as pd

from ai_governance_platform.incident_management.export_incidents import (
    export_incidents,
    export_incidents_to_csv,
    export_incidents_to_json,
)
from ai_governance_platform.incident_management.generate_incidents import (
    generate_incidents_from_governance_outputs,
)


def test_export_incidents_to_csv_creates_file(tmp_path) -> None:
    incidents = generate_incidents_from_governance_outputs()
    path = tmp_path / "incident_register.csv"

    created = export_incidents_to_csv(incidents, path)

    assert created == path
    assert path.exists()
    assert len(pd.read_csv(path)) == len(incidents)


def test_export_incidents_to_json_creates_file(tmp_path) -> None:
    incidents = generate_incidents_from_governance_outputs()
    path = tmp_path / "incident_register.json"

    created = export_incidents_to_json(incidents, path)

    assert created == path
    assert path.exists()
    assert len(json.loads(path.read_text(encoding="utf-8"))) == len(incidents)


def test_export_incidents_creates_csv_and_json(tmp_path) -> None:
    incidents = generate_incidents_from_governance_outputs()
    csv_path, json_path = export_incidents(
        incidents, tmp_path / "incidents.csv", tmp_path / "incidents.json"
    )

    assert csv_path.exists()
    assert json_path.exists()
