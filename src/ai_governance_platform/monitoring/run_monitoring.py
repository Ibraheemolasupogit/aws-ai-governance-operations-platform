"""CLI-style runner for local model and system monitoring summaries."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.monitoring.export_monitoring import export_monitoring
from ai_governance_platform.monitoring.generate_monitoring import (
    generate_sample_monitoring_records,
)
from ai_governance_platform.monitoring.schema import MonitoringRecord


def build_monitoring_summary(
    records: list[MonitoringRecord], csv_path: Path, json_path: Path
) -> dict[str, Any]:
    highest_drift = max(records, key=lambda record: record.drift_score)
    lowest_quality = min(records, key=lambda record: record.quality_score)
    return {
        "total_systems_monitored": len(records),
        "count_by_health_status": dict(
            sorted(Counter(record.health_status for record in records).items())
        ),
        "count_by_retraining_advisory": dict(
            sorted(Counter(record.retraining_advisory for record in records).items())
        ),
        "total_guardrail_violations": sum(
            record.guardrail_violation_count for record in records
        ),
        "total_alert_count": sum(record.alert_count for record in records),
        "highest_drift_system": highest_drift.system_name,
        "highest_drift_score": highest_drift.drift_score,
        "lowest_quality_system": lowest_quality.system_name,
        "lowest_quality_score": lowest_quality.quality_score,
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_monitoring() -> tuple[list[MonitoringRecord], dict[str, Any]]:
    records = generate_sample_monitoring_records()
    csv_path, json_path = export_monitoring(records)
    return records, build_monitoring_summary(records, csv_path, json_path)


def main() -> None:
    records, summary = run_monitoring()
    print("Model and system monitoring completed.")
    print(f"Total systems monitored: {summary['total_systems_monitored']}")
    print("Count by health status:")
    for status, count in summary["count_by_health_status"].items():
        print(f"  - {status}: {count}")
    print("Count by retraining advisory:")
    for advisory, count in summary["count_by_retraining_advisory"].items():
        print(f"  - {advisory}: {count}")
    print(f"Total guardrail violations: {summary['total_guardrail_violations']}")
    print(f"Total alert count: {summary['total_alert_count']}")
    print(
        "Highest drift system: "
        f"{summary['highest_drift_system']} ({summary['highest_drift_score']})"
    )
    print(
        "Lowest quality system: "
        f"{summary['lowest_quality_system']} ({summary['lowest_quality_score']})"
    )
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if records:
        print("Monitoring records are local synthetic results only.")


if __name__ == "__main__":
    main()
