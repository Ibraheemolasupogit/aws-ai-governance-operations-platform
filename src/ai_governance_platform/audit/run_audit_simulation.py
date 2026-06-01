"""CLI-style runner for synthetic audit event simulation."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.audit.export_audit_events import export_audit_events
from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events
from ai_governance_platform.audit.schema import AuditEvent


def build_audit_summary(
    events: list[AuditEvent], csv_path: Path, json_path: Path
) -> dict[str, Any]:
    return {
        "total_audit_events_generated": len(events),
        "count_by_event_category": dict(
            sorted(Counter(event.event_category for event in events).items())
        ),
        "count_by_outcome": dict(sorted(Counter(event.outcome for event in events).items())),
        "count_by_severity": dict(sorted(Counter(event.severity for event in events).items())),
        "production_event_count": sum(event.environment == "production" for event in events),
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_audit_simulation() -> tuple[list[AuditEvent], dict[str, Any]]:
    events = generate_sample_audit_events()
    csv_path, json_path = export_audit_events(events)
    return events, build_audit_summary(events, csv_path, json_path)


def main() -> None:
    events, summary = run_audit_simulation()
    print("Audit event simulation completed.")
    print(f"Total audit events generated: {summary['total_audit_events_generated']}")
    print("Count by event category:")
    for category, count in summary["count_by_event_category"].items():
        print(f"  - {category}: {count}")
    print("Count by outcome:")
    for outcome, count in summary["count_by_outcome"].items():
        print(f"  - {outcome}: {count}")
    print("Count by severity:")
    for severity, count in summary["count_by_severity"].items():
        print(f"  - {severity}: {count}")
    print(f"Production event count: {summary['production_event_count']}")
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if events:
        print("Audit events are local synthetic results only.")


if __name__ == "__main__":
    main()
