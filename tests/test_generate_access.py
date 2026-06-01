from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records


def test_generated_access_records_are_non_empty() -> None:
    records = generate_sample_access_records()

    assert records


def test_generated_access_records_include_warning_and_fail_after_review() -> None:
    reviewed = review_access_records(generate_sample_access_records())
    statuses = {record.finding_status for record in reviewed}

    assert "warning" in statuses
    assert "fail" in statuses


def test_generated_access_records_include_required_cases() -> None:
    records = generate_sample_access_records()

    assert any(
        record.environment == "production" and record.access_level == "admin"
        for record in records
    )
    assert any(record.service_role for record in records)
    assert any(record.access_status == "expired" for record in records)
