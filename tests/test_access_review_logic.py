from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_record


def test_privileged_access_without_mfa_creates_fail_or_warning() -> None:
    record = next(
        record for record in generate_sample_access_records() if record.access_id == "AR-004"
    )

    reviewed = review_access_record(record)

    assert reviewed.finding_status in {"fail", "warning"}
    assert "MFA" in reviewed.finding_reason


def test_expired_access_creates_fail_or_warning() -> None:
    record = next(
        record for record in generate_sample_access_records() if record.access_status == "expired"
    )

    reviewed = review_access_record(record)

    assert reviewed.finding_status in {"fail", "warning"}
    assert "Expired access" in reviewed.finding_reason


def test_service_role_without_clear_justification_warns() -> None:
    record = next(
        record for record in generate_sample_access_records() if record.access_id == "AR-009"
    )

    reviewed = review_access_record(record)

    assert reviewed.finding_status == "warning"
    assert "Service role" in reviewed.finding_reason
