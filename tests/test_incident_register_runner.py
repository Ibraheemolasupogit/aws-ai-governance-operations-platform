from ai_governance_platform.incident_management.run_incident_register import (
    run_incident_register,
)


def test_incident_register_runner_returns_useful_summary() -> None:
    incidents, risks, summary = run_incident_register()

    assert incidents
    assert risks
    assert summary["total_incidents"] == len(incidents)
    assert summary["total_risk_register_entries"] == len(risks)
    assert summary["incidents_by_severity"]
    assert summary["incidents_by_status"]
    assert summary["incidents_by_source"]
    assert summary["risks_by_category"]
    assert summary["risks_by_residual_risk_rating"]
    assert summary["high_critical_incident_count"] > 0
    assert summary["urgent_remediation_count"] > 0
    assert summary["incident_csv_path"].endswith("outputs/incident_register.csv")
    assert summary["risk_csv_path"].endswith("outputs/model_risk_register.csv")
