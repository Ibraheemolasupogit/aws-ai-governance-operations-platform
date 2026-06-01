"""CLI-style runner for local access review simulation."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.access_review.export_access_review import export_access_review
from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records
from ai_governance_platform.access_review.schema import AccessRecord


def build_access_review_summary(
    records: list[AccessRecord], csv_path: Path, json_path: Path
) -> dict[str, Any]:
    status_counts = Counter(record.finding_status for record in records)
    return {
        "total_access_records_reviewed": len(records),
        "pass_count": status_counts["pass"],
        "warning_count": status_counts["warning"],
        "fail_count": status_counts["fail"],
        "privileged_access_count": sum(record.privileged_access for record in records),
        "production_access_count": sum(record.environment == "production" for record in records),
        "expired_access_count": sum(record.access_status == "expired" for record in records),
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_access_review() -> tuple[list[AccessRecord], dict[str, Any]]:
    records = review_access_records(generate_sample_access_records())
    csv_path, json_path = export_access_review(records)
    return records, build_access_review_summary(records, csv_path, json_path)


def main() -> None:
    records, summary = run_access_review()
    print("Access review simulation completed.")
    print(f"Total access records reviewed: {summary['total_access_records_reviewed']}")
    print(f"Pass count: {summary['pass_count']}")
    print(f"Warning count: {summary['warning_count']}")
    print(f"Fail count: {summary['fail_count']}")
    print(f"Privileged access count: {summary['privileged_access_count']}")
    print(f"Production access count: {summary['production_access_count']}")
    print(f"Expired access count: {summary['expired_access_count']}")
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if records:
        print("Access review records are local synthetic results only.")


if __name__ == "__main__":
    main()
