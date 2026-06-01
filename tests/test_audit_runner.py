from ai_governance_platform.audit.run_audit_simulation import run_audit_simulation


def test_audit_runner_returns_useful_summary() -> None:
    events, summary = run_audit_simulation()

    assert events
    assert summary["total_audit_events_generated"] == len(events)
    assert summary["count_by_event_category"]
    assert summary["count_by_outcome"]
    assert summary["count_by_severity"]
    assert summary["production_event_count"] > 0
    assert summary["csv_path"].endswith("outputs/audit_events.csv")
    assert summary["json_path"].endswith("outputs/audit_events.json")
