"""Export governance policy findings."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.policy_checks.schema import PolicyCheckResult

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "governance_findings.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "governance_findings.json"


def _findings_to_dicts(findings: Iterable[PolicyCheckResult]) -> list[dict]:
    return [finding.model_dump(mode="json") for finding in findings]


def export_findings_to_csv(
    findings: Iterable[PolicyCheckResult], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    """Export policy findings to CSV and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_findings_to_dicts(findings)).to_csv(path, index=False)
    return path


def export_findings_to_json(
    findings: Iterable[PolicyCheckResult], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    """Export policy findings to JSON and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_findings_to_dicts(findings), indent=2), encoding="utf-8")
    return path


def export_findings(
    findings: Iterable[PolicyCheckResult],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    """Export policy findings to CSV and JSON."""
    finding_list = list(findings)
    return (
        export_findings_to_csv(finding_list, csv_path),
        export_findings_to_json(finding_list, json_path),
    )
