from ai_governance_platform.reporting.generate_reports import (
    generate_audit_evidence_pack_markdown,
    generate_executive_summary_markdown,
    generate_governance_report_markdown,
    generate_governance_summary,
    generate_model_risk_summary_markdown,
)


def test_governance_summary_has_non_zero_counts() -> None:
    summary = generate_governance_summary()

    assert summary.total_ai_systems > 0
    assert summary.policy_findings_total > 0
    assert summary.risk_register_entries > 0


def test_markdown_reports_contain_expected_headings() -> None:
    assert "# AI Governance Report" in generate_governance_report_markdown()
    assert "# Audit Evidence Pack" in generate_audit_evidence_pack_markdown()
    assert "# Model Risk Register Summary" in generate_model_risk_summary_markdown()
    assert "# Executive Summary" in generate_executive_summary_markdown()


def test_evidence_pack_mentions_synthetic_local_limitations() -> None:
    text = generate_audit_evidence_pack_markdown()

    assert "local and synthetic" in text
    assert "real AWS telemetry" in text


def test_executive_summary_contains_key_risks_and_priority_actions() -> None:
    text = generate_executive_summary_markdown()

    assert "## Key Risks" in text
    assert "## Priority Actions" in text
