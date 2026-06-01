"""Schemas for local CloudTrail-style audit event simulation."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

EventSource = Literal[
    "synthetic_cloudtrail",
    "synthetic_cloudwatch",
    "synthetic_sagemaker",
    "synthetic_bedrock",
    "synthetic_governance_platform",
]
EventCategory = Literal[
    "model_deployment",
    "model_update",
    "access_change",
    "approval_workflow",
    "monitoring_alert",
    "guardrail_change",
    "policy_check",
    "risk_scoring",
    "incident_event",
]
EventOutcome = Literal["success", "failure", "warning"]
EventSeverity = Literal["low", "medium", "high", "critical"]
ActorType = Literal["user", "service_role", "automation", "governance_reviewer"]
AuditEnvironment = Literal["dev", "test", "staging", "production"]


class AuditEvent(BaseModel):
    """Synthetic audit event for governance and operations traceability."""

    event_id: str = Field(min_length=3)
    event_time: datetime
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    event_source: EventSource
    event_name: str = Field(min_length=3)
    event_category: EventCategory
    actor: str = Field(min_length=2)
    actor_type: ActorType
    environment: AuditEnvironment
    outcome: EventOutcome
    severity: EventSeverity
    resource_id: str = Field(min_length=3)
    change_summary: str = Field(min_length=3)
    evidence_reference: str = Field(min_length=3)
