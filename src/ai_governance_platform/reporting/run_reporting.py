"""CLI-style runner for governance reporting."""

from pathlib import Path
from typing import Any

from ai_governance_platform.reporting.export_reports import export_all_reports
from ai_governance_platform.reporting.schema import GovernanceReportSummary


def build_reporting_summary(
    summary: GovernanceReportSummary,
    report_paths: dict[str, Path],
    summary_json: Path,
    summary_csv: Path,
) -> dict[str, Any]:
    return {
        "total_systems": summary.total_ai_systems,
        "high_critical_systems": summary.high_or_critical_risk_systems,
        "total_policy_findings": summary.policy_findings_total,
        "policy_failures": summary.policy_failures,
        "access_failures": summary.access_review_failures,
        "cost_breaches": summary.cost_threshold_breaches,
        "degraded_critical_monitoring_systems": summary.monitoring_degraded_or_critical,
        "open_incidents": summary.open_incidents,
        "high_critical_incidents": summary.high_or_critical_incidents,
        "report_file_paths": {key: str(path) for key, path in report_paths.items()},
        "summary_json_path": str(summary_json),
        "summary_csv_path": str(summary_csv),
    }


def run_reporting() -> tuple[GovernanceReportSummary, dict[str, Any]]:
    summary, report_paths, summary_json, summary_csv = export_all_reports()
    return summary, build_reporting_summary(summary, report_paths, summary_json, summary_csv)


def main() -> None:
    _, summary = run_reporting()
    print("Governance reporting completed.")
    print(f"Total systems: {summary['total_systems']}")
    print(f"High/critical systems: {summary['high_critical_systems']}")
    print(f"Total policy findings: {summary['total_policy_findings']}")
    print(f"Policy failures: {summary['policy_failures']}")
    print(f"Access failures: {summary['access_failures']}")
    print(f"Cost breaches: {summary['cost_breaches']}")
    print(
        "Degraded/critical monitoring systems: "
        f"{summary['degraded_critical_monitoring_systems']}"
    )
    print(f"Open incidents: {summary['open_incidents']}")
    print(f"High/critical incidents: {summary['high_critical_incidents']}")
    print("Report files:")
    for path in summary["report_file_paths"].values():
        print(f"  - {path}")
    print(f"  - {summary['summary_json_path']}")
    print(f"  - {summary['summary_csv_path']}")


if __name__ == "__main__":
    main()
