import json

import pandas as pd

from ai_governance_platform.reporting.export_reports import (
    export_governance_summary,
    export_markdown_reports,
)
from ai_governance_platform.reporting.generate_reports import generate_governance_summary


def test_export_markdown_reports_creates_files(tmp_path) -> None:
    paths = export_markdown_reports(tmp_path)

    assert set(paths) == {
        "governance_report",
        "audit_evidence_pack",
        "model_risk_summary",
        "executive_summary",
    }
    assert all(path.exists() for path in paths.values())


def test_export_summary_csv_and_json(tmp_path) -> None:
    summary = generate_governance_summary()
    json_path, csv_path = export_governance_summary(
        summary, tmp_path / "summary.json", tmp_path / "summary.csv"
    )

    assert json_path.exists()
    assert csv_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["total_ai_systems"] > 0
    assert pd.read_csv(csv_path).iloc[0]["total_ai_systems"] > 0
