from ai_governance_platform.incident_management.remediation import (
    assign_incident_priority,
    derive_target_resolution_date,
    recommend_risk_mitigation,
)


def test_critical_incidents_receive_urgent_priority() -> None:
    assert assign_incident_priority("critical") == "urgent"


def test_high_incidents_receive_high_priority() -> None:
    assert assign_incident_priority("high") == "high"


def test_critical_incidents_receive_faster_target_than_medium() -> None:
    assert derive_target_resolution_date("critical") < derive_target_resolution_date("medium")


def test_mitigation_recommendations_are_non_empty() -> None:
    assert recommend_risk_mitigation("governance", "high")
