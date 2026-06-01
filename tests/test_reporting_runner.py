from ai_governance_platform.reporting.run_reporting import run_reporting


def test_reporting_runner_returns_useful_summary() -> None:
    report, summary = run_reporting()

    assert report.total_ai_systems > 0
    assert summary["total_systems"] == report.total_ai_systems
    assert summary["high_critical_systems"] > 0
    assert summary["total_policy_findings"] > 0
    assert summary["open_incidents"] > 0
    assert summary["report_file_paths"]
    assert summary["summary_json_path"].endswith("outputs/governance_report_summary.json")
    assert summary["summary_csv_path"].endswith("outputs/governance_report_summary.csv")
