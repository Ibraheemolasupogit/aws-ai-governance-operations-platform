"""Schemas for AI governance risk scoring results."""

from typing import Literal

from pydantic import BaseModel, Field

RiskRating = Literal["low", "medium", "high", "critical"]
Priority = Literal["low", "medium", "high", "urgent"]


class RiskScoreResult(BaseModel):
    """System-level governance risk score for one AI system."""

    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    system_type: str = Field(min_length=3)
    risk_tier: str = Field(min_length=3)
    deployment_environment: str = Field(min_length=3)
    business_criticality_score: float = Field(ge=0, le=100)
    data_sensitivity_score: float = Field(ge=0, le=100)
    deployment_exposure_score: float = Field(ge=0, le=100)
    access_risk_score: float = Field(ge=0, le=100)
    monitoring_maturity_score: float = Field(ge=0, le=100)
    cost_risk_score: float = Field(ge=0, le=100)
    compliance_gap_score: float = Field(ge=0, le=100)
    policy_failure_score: float = Field(ge=0, le=100)
    overall_risk_score: float = Field(ge=0, le=100)
    risk_rating: RiskRating
    priority: Priority
    recommended_action: str = Field(min_length=3)
