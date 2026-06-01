from ai_governance_platform.incident_management.generate_incidents import (
    generate_incidents_from_governance_outputs,
)


def test_generated_incidents_are_non_empty_and_varied() -> None:
    incidents = generate_incidents_from_governance_outputs()

    assert incidents
    assert len({incident.incident_type for incident in incidents}) > 4


def test_generated_incidents_include_required_types_and_high_severity() -> None:
    incidents = generate_incidents_from_governance_outputs()
    types = {incident.incident_type for incident in incidents}

    assert "policy_failure" in types
    assert "access_violation" in types
    assert "cost_anomaly" in types
    assert "monitoring_degradation" in types
    assert "drift_alert" in types
    assert "guardrail_violation" in types
    assert any(incident.severity in {"high", "critical"} for incident in incidents)


def test_incidents_include_remediation_metadata() -> None:
    incidents = generate_incidents_from_governance_outputs()

    assert all(incident.owner for incident in incidents)
    assert all(incident.evidence_reference for incident in incidents)
    assert all(incident.recommended_action for incident in incidents)
    assert all(incident.target_resolution_date for incident in incidents)


def test_priority_is_aligned_with_severity() -> None:
    incidents = generate_incidents_from_governance_outputs()
    mapping = {"critical": "urgent", "high": "high", "medium": "medium", "low": "low"}

    assert all(incident.priority == mapping[incident.severity] for incident in incidents)
