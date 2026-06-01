"""Schemas for governance policy check findings."""

from typing import Literal

from pydantic import BaseModel, Field

CheckStatus = Literal["pass", "fail", "warning"]
Severity = Literal["low", "medium", "high", "critical"]
PolicyCategory = Literal[
    "ownership",
    "risk_management",
    "approval",
    "monitoring",
    "documentation",
    "access_control",
    "cost_management",
    "incident_management",
]


class PolicyCheckResult(BaseModel):
    """Result produced by evaluating one governance policy against one AI system."""

    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    policy_name: str = Field(min_length=3)
    policy_category: PolicyCategory
    check_status: CheckStatus
    severity: Severity
    finding: str = Field(min_length=3)
    recommendation: str = Field(min_length=3)
    evidence_field: str = Field(min_length=2)
