from datetime import date

import pytest
from pydantic import ValidationError

from ai_governance_platform.inventory.schema import AISystemRecord


def valid_record_payload() -> dict:
    return {
        "system_id": "AI-999",
        "system_name": "Synthetic Governance Test System",
        "system_type": "genai_llm",
        "model_family": "test-family",
        "owner": "Test Owner",
        "business_unit": "AI Governance",
        "business_use_case": "Validate local inventory schema behavior",
        "risk_tier": "high",
        "lifecycle_status": "validation",
        "deployment_environment": "local",
        "data_sensitivity": "internal",
        "input_data_type": "synthetic prompts",
        "output_type": "synthetic response",
        "aws_service_owner": "AI Platform",
        "primary_aws_services": ["Bedrock", "S3"],
        "approval_status": "pending",
        "monitoring_status": "basic",
        "model_card_status": "draft",
        "access_review_status": "in_progress",
        "cost_center": "CC-TEST-001",
        "created_date": "2026-01-01",
        "last_review_date": "2026-05-01",
    }


def test_ai_system_record_validates_required_fields() -> None:
    record = AISystemRecord.model_validate(valid_record_payload())

    assert record.system_id == "AI-999"
    assert record.risk_tier == "high"
    assert record.system_type == "genai_llm"
    assert record.created_date == date(2026, 1, 1)


@pytest.mark.parametrize("risk_tier", ["low", "medium", "high", "critical"])
def test_allowed_risk_tiers_validate(risk_tier: str) -> None:
    payload = valid_record_payload()
    payload["risk_tier"] = risk_tier

    assert AISystemRecord.model_validate(payload).risk_tier == risk_tier


@pytest.mark.parametrize(
    "system_type",
    [
        "traditional_ml",
        "genai_llm",
        "multimodal_ai",
        "recommendation_system",
        "anomaly_detection",
    ],
)
def test_allowed_system_types_validate(system_type: str) -> None:
    payload = valid_record_payload()
    payload["system_type"] = system_type

    assert AISystemRecord.model_validate(payload).system_type == system_type


def test_invalid_system_id_prefix_fails_validation() -> None:
    payload = valid_record_payload()
    payload["system_id"] = "SYS-999"

    with pytest.raises(ValidationError):
        AISystemRecord.model_validate(payload)
