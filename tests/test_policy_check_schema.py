import pytest
from pydantic import ValidationError

from ai_governance_platform.policy_checks.schema import PolicyCheckResult


def valid_policy_check_payload() -> dict:
    return {
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "policy_name": "owner_required",
        "policy_category": "ownership",
        "check_status": "pass",
        "severity": "high",
        "finding": "AI system has an accountable owner.",
        "recommendation": "Keep the owner current during each governance review.",
        "evidence_field": "owner",
    }


def test_policy_check_result_validates() -> None:
    result = PolicyCheckResult.model_validate(valid_policy_check_payload())

    assert result.system_id == "AI-001"
    assert result.check_status == "pass"
    assert result.policy_category == "ownership"


@pytest.mark.parametrize("check_status", ["pass", "fail", "warning"])
def test_allowed_check_statuses_validate(check_status: str) -> None:
    payload = valid_policy_check_payload()
    payload["check_status"] = check_status

    assert PolicyCheckResult.model_validate(payload).check_status == check_status


def test_invalid_severity_fails_validation() -> None:
    payload = valid_policy_check_payload()
    payload["severity"] = "blocker"

    with pytest.raises(ValidationError):
        PolicyCheckResult.model_validate(payload)
