import json

import pandas as pd

from ai_governance_platform.incident_management.export_risk_register import (
    export_risk_register,
    export_risk_register_to_csv,
    export_risk_register_to_json,
)
from ai_governance_platform.incident_management.generate_risk_register import (
    generate_risk_register,
)


def test_export_risk_register_to_csv_creates_file(tmp_path) -> None:
    risks = generate_risk_register()
    path = tmp_path / "model_risk_register.csv"

    created = export_risk_register_to_csv(risks, path)

    assert created == path
    assert path.exists()
    assert len(pd.read_csv(path)) == len(risks)


def test_export_risk_register_to_json_creates_file(tmp_path) -> None:
    risks = generate_risk_register()
    path = tmp_path / "model_risk_register.json"

    created = export_risk_register_to_json(risks, path)

    assert created == path
    assert path.exists()
    assert len(json.loads(path.read_text(encoding="utf-8"))) == len(risks)


def test_export_risk_register_creates_csv_and_json(tmp_path) -> None:
    risks = generate_risk_register()
    csv_path, json_path = export_risk_register(
        risks, tmp_path / "risks.csv", tmp_path / "risks.json"
    )

    assert csv_path.exists()
    assert json_path.exists()
