from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events


def test_generated_audit_events_are_non_empty() -> None:
    events = generate_sample_audit_events()

    assert events
    assert 30 <= len(events) <= 50


def test_audit_events_include_multiple_categories() -> None:
    events = generate_sample_audit_events()

    assert len({event.event_category for event in events}) >= 8


def test_audit_events_include_required_outcomes_and_severities() -> None:
    events = generate_sample_audit_events()

    assert {"success", "warning", "failure"}.issubset({event.outcome for event in events})
    assert {"low", "medium", "high", "critical"}.issubset(
        {event.severity for event in events}
    )


def test_audit_events_include_production_and_actor_types() -> None:
    events = generate_sample_audit_events()

    assert any(event.environment == "production" for event in events)
    assert {"user", "service_role", "automation", "governance_reviewer"}.issubset(
        {event.actor_type for event in events}
    )
