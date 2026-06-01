"""Export governance reports and summary data."""

import json
from pathlib import Path

import pandas as pd

from ai_governance_platform.reporting.generate_reports import (
    generate_audit_evidence_pack_markdown,
    generate_executive_summary_markdown,
    generate_governance_report_markdown,
    generate_governance_summary,
    generate_model_risk_summary_markdown,
)
from ai_governance_platform.reporting.schema import GovernanceReportSummary

REPORT_DIR = Path("reports")
OUTPUT_DIR = Path("outputs")
GOVERNANCE_REPORT_PATH = REPORT_DIR / "ai_governance_report.md"
AUDIT_EVIDENCE_PATH = REPORT_DIR / "audit_evidence_pack.md"
MODEL_RISK_PATH = REPORT_DIR / "model_risk_register.md"
EXECUTIVE_SUMMARY_PATH = REPORT_DIR / "executive_summary.md"
SUMMARY_JSON_PATH = OUTPUT_DIR / "governance_report_summary.json"
SUMMARY_CSV_PATH = OUTPUT_DIR / "governance_report_summary.csv"


def export_governance_summary(
    summary: GovernanceReportSummary,
    json_path: Path | str = SUMMARY_JSON_PATH,
    csv_path: Path | str = SUMMARY_CSV_PATH,
) -> tuple[Path, Path]:
    json_output = Path(json_path)
    csv_output = Path(csv_path)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    data = summary.model_dump(mode="json")
    json_output.write_text(json.dumps(data, indent=2), encoding="utf-8")
    pd.DataFrame([data]).to_csv(csv_output, index=False)
    return json_output, csv_output


def export_markdown_reports(report_dir: Path | str = REPORT_DIR) -> dict[str, Path]:
    directory = Path(report_dir)
    directory.mkdir(parents=True, exist_ok=True)
    reports = {
        "governance_report": directory / "ai_governance_report.md",
        "audit_evidence_pack": directory / "audit_evidence_pack.md",
        "model_risk_summary": directory / "model_risk_register.md",
        "executive_summary": directory / "executive_summary.md",
    }
    reports["governance_report"].write_text(generate_governance_report_markdown(), encoding="utf-8")
    reports["audit_evidence_pack"].write_text(
        generate_audit_evidence_pack_markdown(), encoding="utf-8"
    )
    reports["model_risk_summary"].write_text(
        generate_model_risk_summary_markdown(), encoding="utf-8"
    )
    reports["executive_summary"].write_text(
        generate_executive_summary_markdown(), encoding="utf-8"
    )
    return reports


def export_all_reports() -> tuple[GovernanceReportSummary, dict[str, Path], Path, Path]:
    summary = generate_governance_summary()
    report_paths = export_markdown_reports()
    summary_json, summary_csv = export_governance_summary(summary)
    return summary, report_paths, summary_json, summary_csv
