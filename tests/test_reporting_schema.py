from ai_governance_platform.reporting.schema import GovernanceReportSummary


def test_governance_report_summary_validates() -> None:
    summary = GovernanceReportSummary(
        report_id="GOV-1",
        report_name="Governance Report",
        report_period="2026-05",
        total_ai_systems=10,
        production_systems=4,
        high_or_critical_risk_systems=4,
        policy_findings_total=80,
        policy_failures=2,
        access_review_failures=3,
        audit_events_total=36,
        cost_threshold_breaches=3,
        monitoring_degraded_or_critical=4,
        open_incidents=24,
        high_or_critical_incidents=24,
        risk_register_entries=42,
        generated_at="2026-06-02T09:00:00",
    )

    assert summary.total_ai_systems == 10
