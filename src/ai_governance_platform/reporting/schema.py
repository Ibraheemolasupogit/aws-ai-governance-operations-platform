"""Schemas for governance reporting summaries."""

from datetime import datetime

from pydantic import BaseModel, Field


class GovernanceReportSummary(BaseModel):
    """Roll-up metrics for local AI governance reporting."""

    report_id: str = Field(min_length=3)
    report_name: str = Field(min_length=3)
    report_period: str = Field(min_length=3)
    total_ai_systems: int = Field(ge=0)
    production_systems: int = Field(ge=0)
    high_or_critical_risk_systems: int = Field(ge=0)
    policy_findings_total: int = Field(ge=0)
    policy_failures: int = Field(ge=0)
    access_review_failures: int = Field(ge=0)
    audit_events_total: int = Field(ge=0)
    cost_threshold_breaches: int = Field(ge=0)
    monitoring_degraded_or_critical: int = Field(ge=0)
    open_incidents: int = Field(ge=0)
    high_or_critical_incidents: int = Field(ge=0)
    risk_register_entries: int = Field(ge=0)
    generated_at: datetime
