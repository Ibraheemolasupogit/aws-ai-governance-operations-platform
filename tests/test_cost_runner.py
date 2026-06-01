from ai_governance_platform.cost_management.run_cost_monitoring import run_cost_monitoring


def test_cost_runner_returns_useful_summary() -> None:
    records, summary = run_cost_monitoring()

    assert records
    assert summary["total_systems_costed"] == len(records)
    assert summary["total_estimated_monthly_cost"] > 0
    assert summary["average_system_cost"] > 0
    assert summary["threshold_breached_count"] > 0
    assert summary["approaching_threshold_count"] > 0
    assert summary["anomaly_count"] > 0
    assert summary["highest_cost_system"]
    assert summary["csv_path"].endswith("outputs/cost_monitoring.csv")
    assert summary["json_path"].endswith("outputs/cost_monitoring.json")
