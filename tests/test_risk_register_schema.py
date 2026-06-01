from ai_governance_platform.incident_management.risk_register_schema import RiskRegisterRecord


def test_risk_register_record_validates() -> None:
    record = RiskRegisterRecord(
        risk_id="RISK-999",
        system_id="AI-001",
        system_name="Retail GenAI Shopping Assistant",
        risk_category="governance",
        risk_description="Synthetic governance risk.",
        inherent_risk_rating="high",
        residual_risk_rating="medium",
        likelihood="possible",
        impact="medium",
        priority="medium",
        owner="Maya Chen",
        business_unit="Digital Commerce",
        control_status="partially_effective",
        control_gap="Synthetic control gap.",
        evidence_reference="outputs/risk_scores.json#AI-001",
        mitigation_plan="Monitor governance controls.",
        review_frequency="semiannual",
        next_review_date="2026-11-28",
        status="monitoring",
    )

    assert record.risk_id == "RISK-999"
    assert record.risk_category == "governance"
