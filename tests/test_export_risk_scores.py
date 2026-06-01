import json

import pandas as pd

from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.risk_scoring.export_scores import (
    export_scores,
    export_scores_to_csv,
    export_scores_to_json,
)
from ai_governance_platform.risk_scoring.scoring import score_inventory


def test_export_scores_to_csv_creates_file(tmp_path) -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))
    output_path = tmp_path / "risk_scores.csv"

    created_path = export_scores_to_csv(scores, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(scores)
    assert "overall_risk_score" in exported.columns


def test_export_scores_to_json_creates_file(tmp_path) -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))
    output_path = tmp_path / "risk_scores.json"

    created_path = export_scores_to_json(scores, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(scores)
    assert "overall_risk_score" in exported[0]


def test_export_scores_creates_csv_and_json(tmp_path) -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))
    csv_path = tmp_path / "risk_scores.csv"
    json_path = tmp_path / "risk_scores.json"

    created_csv_path, created_json_path = export_scores(scores, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
