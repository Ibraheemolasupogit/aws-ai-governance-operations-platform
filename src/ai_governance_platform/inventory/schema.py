"""Schemas for local AI system inventory records."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

SystemType = Literal[
    "traditional_ml",
    "genai_llm",
    "multimodal_ai",
    "recommendation_system",
    "anomaly_detection",
]
RiskTier = Literal["low", "medium", "high", "critical"]
LifecycleStatus = Literal["experimental", "validation", "approved", "production", "retired"]
DeploymentEnvironment = Literal["local", "dev", "test", "staging", "production"]
DataSensitivity = Literal["public", "internal", "confidential", "restricted"]
ApprovalStatus = Literal["pending", "approved", "rejected", "not_required"]
MonitoringStatus = Literal["not_enabled", "basic", "enhanced", "production_ready"]
ModelCardStatus = Literal["missing", "draft", "complete"]
AccessReviewStatus = Literal["not_started", "in_progress", "complete", "overdue"]


class AISystemRecord(BaseModel):
    """Validated local inventory record for an ML or GenAI system."""

    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    system_type: SystemType
    model_family: str = Field(min_length=2)
    owner: str = Field(min_length=2)
    business_unit: str = Field(min_length=2)
    business_use_case: str = Field(min_length=5)
    risk_tier: RiskTier
    lifecycle_status: LifecycleStatus
    deployment_environment: DeploymentEnvironment
    data_sensitivity: DataSensitivity
    input_data_type: str = Field(min_length=2)
    output_type: str = Field(min_length=2)
    aws_service_owner: str = Field(min_length=2)
    primary_aws_services: list[str] = Field(min_length=1)
    approval_status: ApprovalStatus
    monitoring_status: MonitoringStatus
    model_card_status: ModelCardStatus
    access_review_status: AccessReviewStatus
    cost_center: str = Field(min_length=2)
    created_date: date
    last_review_date: date

    @field_validator("system_id")
    @classmethod
    def system_id_must_use_expected_prefix(cls, value: str) -> str:
        if not value.startswith("AI-"):
            msg = "system_id must start with 'AI-'"
            raise ValueError(msg)
        return value

    @field_validator("primary_aws_services")
    @classmethod
    def aws_services_must_not_be_blank(cls, value: list[str]) -> list[str]:
        if any(not service.strip() for service in value):
            msg = "primary_aws_services cannot contain blank service names"
            raise ValueError(msg)
        return value

    @field_validator("last_review_date")
    @classmethod
    def last_review_date_must_not_precede_created_date(cls, value: date, info) -> date:
        created_date = info.data.get("created_date")
        if created_date and value < created_date:
            msg = "last_review_date cannot be before created_date"
            raise ValueError(msg)
        return value
