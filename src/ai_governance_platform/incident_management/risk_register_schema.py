"""Schemas for local AI risk register records."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

RiskCategory = Literal[
    "governance",
    "access_control",
    "model_performance",
    "responsible_ai",
    "cost_management",
    "operational_resilience",
    "auditability",
    "data_sensitivity",
]
RiskRating = Literal["low", "medium", "high", "critical"]
Likelihood = Literal["rare", "unlikely", "possible", "likely", "almost_certain"]
Impact = Literal["low", "medium", "high", "severe"]
ControlStatus = Literal["effective", "partially_effective", "ineffective", "not_assessed"]
RiskStatus = Literal["open", "monitoring", "mitigating", "accepted", "closed"]
Priority = Literal["low", "medium", "high", "urgent"]


class RiskRegisterRecord(BaseModel):
    """System-level risk register entry."""

    risk_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    risk_category: RiskCategory
    risk_description: str = Field(min_length=3)
    inherent_risk_rating: RiskRating
    residual_risk_rating: RiskRating
    likelihood: Likelihood
    impact: Impact
    priority: Priority
    owner: str = Field(min_length=2)
    business_unit: str = Field(min_length=2)
    control_status: ControlStatus
    control_gap: str = Field(min_length=3)
    evidence_reference: str = Field(min_length=3)
    mitigation_plan: str = Field(min_length=3)
    review_frequency: str = Field(min_length=3)
    next_review_date: date
    status: RiskStatus
