from ai_governance_platform.incident_management.schema import IncidentRecord


def test_incident_record_validates() -> None:
    record = IncidentRecord(
        incident_id="INC-999",
        system_id="AI-001",
        system_name="Retail GenAI Shopping Assistant",
        incident_type="policy_failure",
        severity="high",
        status="open",
        priority="high",
        source="policy_checks",
        detected_date="2026-06-01",
        owner="Maya Chen",
        business_unit="Digital Commerce",
        description="Synthetic policy failure.",
        evidence_reference="outputs/governance_findings.json#AI-001",
        recommended_action="Remediate failed governance control.",
        remediation_status="not_started",
        target_resolution_date="2026-06-15",
        residual_risk="medium",
    )

    assert record.incident_id == "INC-999"
    assert record.priority == "high"
