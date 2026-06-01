"""Schemas for local AI incident register records."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

IncidentType = Literal[
    "policy_failure",
    "access_violation",
    "cost_anomaly",
    "monitoring_degradation",
    "drift_alert",
    "guardrail_violation",
    "audit_failure",
    "operational_failure",
]
Severity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["open", "investigating", "remediating", "resolved", "accepted_risk"]
Priority = Literal["low", "medium", "high", "urgent"]
IncidentSource = Literal[
    "policy_checks",
    "access_review",
    "audit_events",
    "cost_monitoring",
    "model_monitoring",
    "risk_scoring",
]
RemediationStatus = Literal["not_started", "in_progress", "completed", "accepted", "overdue"]
ResidualRisk = Literal["low", "medium", "high", "critical"]


class IncidentRecord(BaseModel):
    """Actionable incident derived from local governance and operations signals."""

    incident_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus
    priority: Priority
    source: IncidentSource
    detected_date: date
    owner: str = Field(min_length=2)
    business_unit: str = Field(min_length=2)
    description: str = Field(min_length=3)
    evidence_reference: str = Field(min_length=3)
    recommended_action: str = Field(min_length=3)
    remediation_status: RemediationStatus
    target_resolution_date: date
    closure_date: date | None = None
    residual_risk: ResidualRisk
