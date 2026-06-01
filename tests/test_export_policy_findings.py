import json

import pandas as pd

from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.policy_checks.export_findings import (
    export_findings,
    export_findings_to_csv,
    export_findings_to_json,
)


def test_export_findings_to_csv_creates_file(tmp_path) -> None:
    findings = run_policy_checks(generate_sample_inventory())
    output_path = tmp_path / "governance_findings.csv"

    created_path = export_findings_to_csv(findings, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(findings)
    assert "policy_name" in exported.columns


def test_export_findings_to_json_creates_file(tmp_path) -> None:
    findings = run_policy_checks(generate_sample_inventory())
    output_path = tmp_path / "governance_findings.json"

    created_path = export_findings_to_json(findings, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(findings)
    assert "policy_name" in exported[0]


def test_export_findings_creates_csv_and_json(tmp_path) -> None:
    findings = run_policy_checks(generate_sample_inventory())
    csv_path = tmp_path / "governance_findings.csv"
    json_path = tmp_path / "governance_findings.json"

    created_csv_path, created_json_path = export_findings(findings, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
