from ai_governance_platform.cost_management.checks import (
    calculate_estimated_total_cost,
    evaluate_cost_anomaly,
    evaluate_threshold_status,
)
from ai_governance_platform.cost_management.schema import CostRecord


def make_cost_record(**updates) -> CostRecord:
    payload = {
        "cost_record_id": "COST-900",
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "system_type": "genai_llm",
        "cost_center": "CC-TEST",
        "billing_period": "2026-05",
        "estimated_bedrock_cost": 100,
        "estimated_sagemaker_endpoint_cost": 10,
        "estimated_training_cost": 20,
        "estimated_inference_cost": 30,
        "estimated_storage_cost": 40,
        "estimated_total_cost": 200,
        "monthly_threshold": 1000,
    }
    payload.update(updates)
    return CostRecord.model_validate(payload)


def test_total_cost_is_calculated_correctly() -> None:
    record = make_cost_record()

    assert calculate_estimated_total_cost(record) == 200


def test_threshold_status_logic() -> None:
    assert evaluate_threshold_status(799, 1000) == "within_threshold"
    assert evaluate_threshold_status(800, 1000) == "approaching_threshold"
    assert evaluate_threshold_status(1000, 1000) == "breached"


def test_anomaly_status_detects_high_genai_cost() -> None:
    record = make_cost_record(
        estimated_bedrock_cost=850,
        estimated_total_cost=950,
        monthly_threshold=1000,
    )

    assert evaluate_cost_anomaly(record)[0] == "anomaly"
