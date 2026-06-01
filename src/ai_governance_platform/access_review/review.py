"""Local IAM-style access review checks."""

from collections.abc import Iterable
from datetime import date

from ai_governance_platform.access_review.schema import AccessRecord

RECENT_REVIEW_CUTOFF = date(2026, 1, 1)


def privileged_access_requires_mfa(record: AccessRecord) -> tuple[str, str] | None:
    if record.privileged_access and not record.mfa_enabled:
        return "fail", "Privileged access does not have MFA enabled."
    return None


def production_admin_requires_justification(record: AccessRecord) -> tuple[str, str] | None:
    is_production_admin = record.environment == "production" and record.access_level == "admin"
    if is_production_admin and len(record.business_justification.strip()) < 25:
        return "warning", "Production admin access has weak business justification."
    return None


def expired_access_should_be_removed(record: AccessRecord) -> tuple[str, str] | None:
    if record.access_status == "expired" or record.expiry_date < date.today():
        return "fail", "Expired access should be removed or formally revoked."
    if record.access_status == "pending_removal":
        return "warning", "Access is pending removal and should be tracked to completion."
    return None


def service_roles_should_have_clear_justification(record: AccessRecord) -> tuple[str, str] | None:
    if record.service_role and len(record.business_justification.strip()) < 25:
        return "warning", "Service role access lacks clear business justification."
    return None


def production_access_requires_recent_review(record: AccessRecord) -> tuple[str, str] | None:
    if record.environment == "production" and record.last_review_date < RECENT_REVIEW_CUTOFF:
        return "warning", "Production access has not been reviewed recently."
    return None


def owner_access_should_be_limited(record: AccessRecord) -> tuple[str, str] | None:
    if record.access_level == "owner" and record.environment == "production":
        return "warning", "Production owner access should be limited and periodically recertified."
    return None


def revoked_access_should_not_be_active(record: AccessRecord) -> tuple[str, str] | None:
    if record.access_status == "revoked" and record.expiry_date > date.today():
        return "warning", "Revoked access still has a future expiry date in the source record."
    return None


ACCESS_REVIEW_CHECKS = [
    privileged_access_requires_mfa,
    production_admin_requires_justification,
    expired_access_should_be_removed,
    service_roles_should_have_clear_justification,
    production_access_requires_recent_review,
    owner_access_should_be_limited,
    revoked_access_should_not_be_active,
]


def review_access_record(record: AccessRecord) -> AccessRecord:
    """Apply access review checks and return a reviewed record."""
    findings = [check(record) for check in ACCESS_REVIEW_CHECKS]
    active_findings = [finding for finding in findings if finding is not None]

    if not active_findings:
        return record.model_copy(
            update={
                "finding_status": "pass",
                "finding_reason": "No access review issues identified.",
                "recommended_action": "Retain access and review on the next cycle.",
            }
        )

    status = "fail" if any(finding[0] == "fail" for finding in active_findings) else "warning"
    reasons = [finding[1] for finding in active_findings]
    action = (
        "Remove or remediate access before the next governance review."
        if status == "fail"
        else "Review and document the access exception or remediation plan."
    )
    return record.model_copy(
        update={
            "finding_status": status,
            "finding_reason": " ".join(reasons),
            "recommended_action": action,
        }
    )


def review_access_records(records: Iterable[AccessRecord]) -> list[AccessRecord]:
    """Apply access review checks to all records."""
    return [review_access_record(record) for record in records]
