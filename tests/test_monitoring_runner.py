from ai_governance_platform.monitoring.run_monitoring import run_monitoring


def test_monitoring_runner_returns_useful_summary() -> None:
    records, summary = run_monitoring()

    assert records
    assert summary["total_systems_monitored"] == len(records)
    assert summary["count_by_health_status"]
    assert summary["count_by_retraining_advisory"]
    assert summary["total_guardrail_violations"] > 0
    assert summary["total_alert_count"] > 0
    assert summary["highest_drift_system"]
    assert summary["lowest_quality_system"]
    assert summary["csv_path"].endswith("outputs/model_monitoring.csv")
    assert summary["json_path"].endswith("outputs/model_monitoring.json")
