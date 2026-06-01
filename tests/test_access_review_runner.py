from ai_governance_platform.access_review.run_access_review import run_access_review


def test_access_review_runner_returns_useful_summary() -> None:
    records, summary = run_access_review()

    assert records
    assert summary["total_access_records_reviewed"] == len(records)
    assert summary["warning_count"] > 0
    assert summary["fail_count"] > 0
    assert summary["privileged_access_count"] > 0
    assert summary["production_access_count"] > 0
    assert summary["expired_access_count"] > 0
    assert summary["csv_path"].endswith("outputs/access_review.csv")
    assert summary["json_path"].endswith("outputs/access_review.json")
