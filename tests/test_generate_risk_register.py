from ai_governance_platform.incident_management.generate_risk_register import (
    generate_risk_register,
)


def test_generated_risk_register_is_non_empty_and_varied() -> None:
    risks = generate_risk_register()

    assert risks
    assert len({risk.risk_category for risk in risks}) > 5


def test_risk_register_contains_high_or_critical_residual_risk() -> None:
    risks = generate_risk_register()

    assert any(risk.residual_risk_rating in {"high", "critical"} for risk in risks)


def test_risks_include_required_metadata() -> None:
    risks = generate_risk_register()

    assert all(risk.owner for risk in risks)
    assert all(risk.mitigation_plan for risk in risks)
    assert all(risk.evidence_reference for risk in risks)
    assert all(risk.next_review_date for risk in risks)


def test_review_frequency_is_derived() -> None:
    risks = generate_risk_register()
    allowed = {"monthly", "quarterly", "semiannual", "annual"}

    assert {risk.review_frequency for risk in risks}.issubset(allowed)
