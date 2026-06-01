from datetime import datetime

import pytest
from pydantic import ValidationError

from ai_governance_platform.audit.schema import AuditEvent


def valid_audit_payload() -> dict:
    return {
        "event_id": "EVT-999",
        "event_time": "2026-05-01T10:15:00",
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "event_source": "synthetic_cloudtrail",
        "event_name": "GrantAccess",
        "event_category": "access_change",
        "actor": "test.user",
        "actor_type": "user",
        "environment": "production",
        "outcome": "success",
        "severity": "medium",
        "resource_id": "ai-001-access",
        "change_summary": "Synthetic access grant event.",
        "evidence_reference": "outputs/evidence/ai-001/999.json",
    }


def test_audit_event_validates() -> None:
    event = AuditEvent.model_validate(valid_audit_payload())

    assert event.event_id == "EVT-999"
    assert isinstance(event.event_time, datetime)
    assert event.event_category == "access_change"


def test_invalid_outcome_fails_validation() -> None:
    payload = valid_audit_payload()
    payload["outcome"] = "partial"

    with pytest.raises(ValidationError):
        AuditEvent.model_validate(payload)
