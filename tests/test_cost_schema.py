import pytest
from pydantic import ValidationError

from ai_governance_platform.cost_management.schema import CostRecord


def valid_cost_payload() -> dict:
    return {
        "cost_record_id": "COST-999",
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "system_type": "genai_llm",
        "cost_center": "CC-TEST",
        "billing_period": "2026-05",
        "estimated_bedrock_cost": 100,
        "estimated_sagemaker_endpoint_cost": 0,
        "estimated_training_cost": 20,
        "estimated_inference_cost": 30,
        "estimated_storage_cost": 10,
        "estimated_total_cost": 160,
        "monthly_threshold": 1000,
        "threshold_status": "within_threshold",
        "anomaly_status": "normal",
        "anomaly_reason": "No anomaly detected.",
        "recommended_action": "Continue standard cost monitoring.",
    }


def test_cost_record_validates() -> None:
    record = CostRecord.model_validate(valid_cost_payload())

    assert record.cost_record_id == "COST-999"
    assert record.estimated_total_cost == 160
    assert record.threshold_status == "within_threshold"


def test_negative_cost_fails_validation() -> None:
    payload = valid_cost_payload()
    payload["estimated_bedrock_cost"] = -1

    with pytest.raises(ValidationError):
        CostRecord.model_validate(payload)
