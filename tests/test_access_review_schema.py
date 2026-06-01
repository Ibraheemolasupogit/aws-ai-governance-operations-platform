from datetime import date

import pytest
from pydantic import ValidationError

from ai_governance_platform.access_review.schema import AccessRecord


def valid_access_payload() -> dict:
    return {
        "access_id": "AR-999",
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "principal_id": "USR-999",
        "principal_name": "Test User",
        "principal_type": "user",
        "role_name": "TestRole",
        "access_level": "analyst",
        "environment": "production",
        "business_justification": "Synthetic test access for validation.",
        "access_status": "active",
        "last_review_date": "2026-04-01",
        "expiry_date": "2026-12-31",
        "mfa_enabled": True,
        "privileged_access": False,
        "service_role": False,
        "finding_status": "pass",
        "finding_reason": "No issue.",
        "recommended_action": "Retain access.",
    }


def test_access_record_validates() -> None:
    record = AccessRecord.model_validate(valid_access_payload())

    assert record.access_id == "AR-999"
    assert record.last_review_date == date(2026, 4, 1)
    assert record.finding_status == "pass"


def test_invalid_access_level_fails_validation() -> None:
    payload = valid_access_payload()
    payload["access_level"] = "super_admin"

    with pytest.raises(ValidationError):
        AccessRecord.model_validate(payload)
