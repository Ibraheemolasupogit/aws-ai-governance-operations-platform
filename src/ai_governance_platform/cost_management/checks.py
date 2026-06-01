"""Local AI platform cost checks."""

from pathlib import Path
from typing import Any

import yaml

from ai_governance_platform.cost_management.schema import CostRecord

DEFAULT_COST_CONFIG_PATH = Path("config/cost_thresholds.yaml")
GENAI_SYSTEM_TYPES = {"genai_llm", "multimodal_ai"}


def load_cost_threshold_config(
    config_path: Path | str = DEFAULT_COST_CONFIG_PATH,
) -> dict[str, Any]:
    """Load local cost threshold configuration."""
    path = Path(config_path)
    with path.open(encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}


def calculate_estimated_total_cost(record: CostRecord) -> float:
    """Calculate estimated total monthly cost from cost components."""
    return round(
        record.estimated_bedrock_cost
        + record.estimated_sagemaker_endpoint_cost
        + record.estimated_training_cost
        + record.estimated_inference_cost
        + record.estimated_storage_cost,
        2,
    )


def evaluate_threshold_status(total_cost: float, monthly_threshold: float) -> str:
    """Evaluate threshold status using 80 percent and 100 percent threshold bands."""
    threshold_ratio = total_cost / monthly_threshold
    if threshold_ratio >= 1:
        return "breached"
    if threshold_ratio >= 0.8:
        return "approaching_threshold"
    return "within_threshold"


def evaluate_cost_anomaly(record: CostRecord) -> tuple[str, str]:
    """Evaluate local cost anomaly status from proxy cost patterns."""
    if record.estimated_total_cost > record.monthly_threshold * 1.25:
        return "anomaly", "Estimated monthly cost is more than 125 percent of threshold."
    if record.system_type in GENAI_SYSTEM_TYPES and record.estimated_bedrock_cost > 700:
        return "anomaly", "GenAI Bedrock-style usage is unusually high for this system."
    if record.estimated_total_cost > record.monthly_threshold * 0.8:
        return "advisory", "Estimated monthly cost is approaching the configured threshold."
    if record.estimated_training_cost > 500 and record.estimated_sagemaker_endpoint_cost == 0:
        return "advisory", "Training cost is elevated for a non-endpoint workload."
    return "normal", "No anomaly detected."


def recommend_cost_action(threshold_status: str, anomaly_status: str) -> str:
    """Recommend a cost governance action."""
    if threshold_status == "breached" or anomaly_status == "anomaly":
        return "Escalate cost review and identify remediation actions."
    if threshold_status == "approaching_threshold" or anomaly_status == "advisory":
        return "Review usage trend and confirm cost owner acknowledgement."
    return "Continue standard cost monitoring."


def evaluate_cost_record(record: CostRecord) -> CostRecord:
    """Evaluate threshold and anomaly status for one cost record."""
    total_cost = calculate_estimated_total_cost(record)
    threshold_status = evaluate_threshold_status(total_cost, record.monthly_threshold)
    anomaly_status, anomaly_reason = evaluate_cost_anomaly(
        record.model_copy(update={"estimated_total_cost": total_cost})
    )
    return record.model_copy(
        update={
            "estimated_total_cost": total_cost,
            "threshold_status": threshold_status,
            "anomaly_status": anomaly_status,
            "anomaly_reason": anomaly_reason,
            "recommended_action": recommend_cost_action(threshold_status, anomaly_status),
        }
    )
