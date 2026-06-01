"""Schemas for local IAM-style AI system access review records."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

PrincipalType = Literal["user", "group", "service_role", "application"]
AccessLevel = Literal["read_only", "analyst", "developer", "operator", "admin", "owner"]
AccessEnvironment = Literal["dev", "test", "staging", "production"]
AccessStatus = Literal["active", "expired", "pending_removal", "revoked"]
FindingStatus = Literal["pass", "warning", "fail"]


class AccessRecord(BaseModel):
    """Synthetic access entitlement and review finding for one AI system."""

    access_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    principal_id: str = Field(min_length=3)
    principal_name: str = Field(min_length=2)
    principal_type: PrincipalType
    role_name: str = Field(min_length=3)
    access_level: AccessLevel
    environment: AccessEnvironment
    business_justification: str = ""
    access_status: AccessStatus
    last_review_date: date
    expiry_date: date
    mfa_enabled: bool
    privileged_access: bool
    service_role: bool
    finding_status: FindingStatus = "pass"
    finding_reason: str = "Pending review."
    recommended_action: str = "Run access review checks."
