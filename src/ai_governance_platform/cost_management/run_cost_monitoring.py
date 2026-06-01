"""CLI-style runner for local AI platform cost monitoring."""

from pathlib import Path
from statistics import mean
from typing import Any

from ai_governance_platform.cost_management.export_costs import export_costs
from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records
from ai_governance_platform.cost_management.schema import CostRecord


def build_cost_summary(
    records: list[CostRecord], csv_path: Path, json_path: Path
) -> dict[str, Any]:
    highest_cost = max(records, key=lambda record: record.estimated_total_cost)
    total_cost = round(sum(record.estimated_total_cost for record in records), 2)
    return {
        "total_systems_costed": len(records),
        "total_estimated_monthly_cost": total_cost,
        "average_system_cost": round(mean(record.estimated_total_cost for record in records), 2),
        "threshold_breached_count": sum(
            record.threshold_status == "breached" for record in records
        ),
        "approaching_threshold_count": sum(
            record.threshold_status == "approaching_threshold" for record in records
        ),
        "anomaly_count": sum(record.anomaly_status == "anomaly" for record in records),
        "highest_cost_system": highest_cost.system_name,
        "highest_cost_amount": highest_cost.estimated_total_cost,
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_cost_monitoring() -> tuple[list[CostRecord], dict[str, Any]]:
    records = generate_sample_cost_records()
    csv_path, json_path = export_costs(records)
    return records, build_cost_summary(records, csv_path, json_path)


def main() -> None:
    records, summary = run_cost_monitoring()
    print("AI platform cost monitoring completed.")
    print(f"Total systems costed: {summary['total_systems_costed']}")
    print(f"Total estimated monthly cost: {summary['total_estimated_monthly_cost']}")
    print(f"Average system cost: {summary['average_system_cost']}")
    print(f"Threshold breached count: {summary['threshold_breached_count']}")
    print(f"Approaching threshold count: {summary['approaching_threshold_count']}")
    print(f"Anomaly count: {summary['anomaly_count']}")
    print(
        "Highest cost system: "
        f"{summary['highest_cost_system']} ({summary['highest_cost_amount']})"
    )
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if records:
        print("Cost monitoring records are local synthetic results only.")


if __name__ == "__main__":
    main()
