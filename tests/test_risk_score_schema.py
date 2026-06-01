import pytest
from pydantic import ValidationError

from ai_governance_platform.risk_scoring.schema import RiskScoreResult


def valid_risk_score_payload() -> dict:
    return {
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "system_type": "genai_llm",
        "risk_tier": "high",
        "deployment_environment": "production",
        "business_criticality_score": 73.0,
        "data_sensitivity_score": 65.0,
        "deployment_exposure_score": 87.5,
        "access_risk_score": 10.0,
        "monitoring_maturity_score": 10.0,
        "cost_risk_score": 65.0,
        "compliance_gap_score": 30.0,
        "policy_failure_score": 0.0,
        "overall_risk_score": 52.3,
        "risk_rating": "high",
        "priority": "high",
        "recommended_action": "Prioritise remediation and owner review.",
    }


def test_risk_score_result_validates() -> None:
    result = RiskScoreResult.model_validate(valid_risk_score_payload())

    assert result.system_id == "AI-001"
    assert result.risk_rating == "high"
    assert result.priority == "high"


@pytest.mark.parametrize("risk_rating", ["low", "medium", "high", "critical"])
def test_allowed_risk_ratings_validate(risk_rating: str) -> None:
    payload = valid_risk_score_payload()
    payload["risk_rating"] = risk_rating

    assert RiskScoreResult.model_validate(payload).risk_rating == risk_rating


@pytest.mark.parametrize("priority", ["low", "medium", "high", "urgent"])
def test_allowed_priorities_validate(priority: str) -> None:
    payload = valid_risk_score_payload()
    payload["priority"] = priority

    assert RiskScoreResult.model_validate(payload).priority == priority


def test_score_above_100_fails_validation() -> None:
    payload = valid_risk_score_payload()
    payload["overall_risk_score"] = 101

    with pytest.raises(ValidationError):
        RiskScoreResult.model_validate(payload)
