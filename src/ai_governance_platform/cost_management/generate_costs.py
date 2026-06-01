"""Generate synthetic AI platform cost records."""

from ai_governance_platform.cost_management.checks import (
    evaluate_cost_record,
    load_cost_threshold_config,
)
from ai_governance_platform.cost_management.schema import CostRecord
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory


def _base_threshold_for_system(system_type: str) -> float:
    config = load_cost_threshold_config()
    thresholds = config.get("monthly_thresholds_usd", {})
    if system_type in {"genai_llm", "multimodal_ai"}:
        return float(thresholds.get("bedrock_usage", 500)) + 400
    if system_type in {"traditional_ml", "recommendation_system", "anomaly_detection"}:
        return float(thresholds.get("sagemaker_endpoint", 1000)) + 300
    return float(thresholds.get("total_ai_platform_cost", 3000))


def generate_sample_cost_records() -> list[CostRecord]:
    """Return deterministic synthetic monthly cost records."""
    inventory = generate_sample_inventory()
    cost_profiles = {
        "AI-001": (720, 0, 80, 220, 60, 1000),
        "AI-002": (0, 420, 560, 90, 45, 1300),
        "AI-003": (0, 250, 40, 160, 35, 900),
        "AI-004": (0, 1180, 180, 420, 80, 1500),
        "AI-005": (0, 680, 120, 260, 55, 1300),
        "AI-006": (260, 0, 45, 120, 30, 900),
        "AI-007": (90, 0, 30, 45, 20, 900),
        "AI-008": (0, 180, 35, 80, 20, 900),
        "AI-009": (0, 760, 240, 410, 70, 1500),
        "AI-010": (820, 0, 95, 180, 45, 900),
    }
    records = []
    for index, system in enumerate(inventory, 1):
        bedrock, endpoint, training, inference, storage, threshold = cost_profiles.get(
            system.system_id,
            (0, 100, 25, 50, 15, _base_threshold_for_system(system.system_type)),
        )
        record = CostRecord(
            cost_record_id=f"COST-{index:03d}",
            system_id=system.system_id,
            system_name=system.system_name,
            system_type=system.system_type,
            cost_center=system.cost_center,
            billing_period="2026-05",
            estimated_bedrock_cost=bedrock,
            estimated_sagemaker_endpoint_cost=endpoint,
            estimated_training_cost=training,
            estimated_inference_cost=inference,
            estimated_storage_cost=storage,
            estimated_total_cost=0,
            monthly_threshold=threshold,
        )
        records.append(evaluate_cost_record(record))
    return records
