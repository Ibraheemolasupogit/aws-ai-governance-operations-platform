"""Schemas for local model and system monitoring summaries."""

from typing import Literal

from pydantic import BaseModel, Field

HealthStatus = Literal["healthy", "watch", "degraded", "critical"]
RetrainingAdvisory = Literal["not_required", "monitor", "recommended", "urgent"]


class MonitoringRecord(BaseModel):
    """Synthetic CloudWatch-style monitoring summary for one AI system."""

    monitoring_record_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    system_type: str = Field(min_length=3)
    monitoring_period: str = Field(min_length=7)
    deployment_environment: str = Field(min_length=3)
    prediction_volume: int = Field(ge=0)
    average_latency_ms: float = Field(ge=0)
    p95_latency_ms: float = Field(ge=0)
    error_rate_percent: float = Field(ge=0)
    drift_score: float = Field(ge=0, le=1)
    quality_score: float = Field(ge=0, le=1)
    guardrail_violation_count: int = Field(ge=0)
    hallucination_risk_flags: int = Field(ge=0)
    availability_percent: float = Field(ge=0, le=100)
    monitoring_status: str = Field(min_length=3)
    health_status: HealthStatus = "healthy"
    retraining_advisory: RetrainingAdvisory = "not_required"
    alert_count: int = Field(ge=0)
    recommended_action: str = "Continue standard monitoring."
