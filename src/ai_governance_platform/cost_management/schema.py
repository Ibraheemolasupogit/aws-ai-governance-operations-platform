"""Schemas for local AI platform cost monitoring."""

from typing import Literal

from pydantic import BaseModel, Field

ThresholdStatus = Literal["within_threshold", "approaching_threshold", "breached"]
AnomalyStatus = Literal["normal", "advisory", "anomaly"]


class CostRecord(BaseModel):
    """Synthetic monthly cost record for one AI system."""

    cost_record_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    system_type: str = Field(min_length=3)
    cost_center: str = Field(min_length=2)
    billing_period: str = Field(min_length=7)
    estimated_bedrock_cost: float = Field(ge=0)
    estimated_sagemaker_endpoint_cost: float = Field(ge=0)
    estimated_training_cost: float = Field(ge=0)
    estimated_inference_cost: float = Field(ge=0)
    estimated_storage_cost: float = Field(ge=0)
    estimated_total_cost: float = Field(ge=0)
    monthly_threshold: float = Field(gt=0)
    threshold_status: ThresholdStatus = "within_threshold"
    anomaly_status: AnomalyStatus = "normal"
    anomaly_reason: str = "No anomaly detected."
    recommended_action: str = "Continue standard cost monitoring."
