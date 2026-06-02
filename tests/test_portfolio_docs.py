from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINAL_DOCS = [
    "docs/runbook.md",
    "docs/portfolio_summary.md",
    "docs/interview_talking_points.md",
    "docs/cv_bullets.md",
    "docs/linkedin_summary.md",
    "docs/github_topics.md",
    "docs/final_checklist.md",
]

README_SECTIONS = [
    "## Problem Statement",
    "## What The Platform Does",
    "## Architecture Overview",
    "## Local-Only Implementation Note",
    "## Commands By Module",
    "## Generated Outputs",
    "## AWS Service Mapping",
    "## Skills Demonstrated",
    "## Portfolio Positioning",
    "## Future Enhancements",
    "## Disclaimer",
]

MODULE_COMMANDS = [
    "ai_governance_platform.inventory.run_inventory",
    "ai_governance_platform.policy_checks.run_policy_checks",
    "ai_governance_platform.risk_scoring.run_risk_scoring",
    "ai_governance_platform.access_review.run_access_review",
    "ai_governance_platform.audit.run_audit_simulation",
    "ai_governance_platform.cost_management.run_cost_monitoring",
    "ai_governance_platform.monitoring.run_monitoring",
    "ai_governance_platform.incident_management.run_incident_register",
    "ai_governance_platform.model_cards.run_model_cards",
    "ai_governance_platform.reporting.run_reporting",
]


def test_final_polish_docs_exist() -> None:
    missing = [path for path in FINAL_DOCS if not (PROJECT_ROOT / path).exists()]

    assert missing == []


def test_readme_contains_key_sections() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    for section in README_SECTIONS:
        assert section in readme


def test_runbook_contains_key_commands() -> None:
    runbook = (PROJECT_ROOT / "docs/runbook.md").read_text(encoding="utf-8")

    assert "python3 -m pytest" in runbook
    assert "python3 -m ruff check ." in runbook
    for command in MODULE_COMMANDS:
        assert command in runbook


def test_portfolio_material_docs_contain_expected_content() -> None:
    assert "senior-level" in (PROJECT_ROOT / "docs/portfolio_summary.md").read_text(
        encoding="utf-8"
    ).lower()
    assert "60-second project pitch" in (
        PROJECT_ROOT / "docs/interview_talking_points.md"
    ).read_text(encoding="utf-8").lower()
    assert "Data Scientist" in (PROJECT_ROOT / "docs/cv_bullets.md").read_text(
        encoding="utf-8"
    )
    assert "LinkedIn" in (PROJECT_ROOT / "docs/linkedin_summary.md").read_text(
        encoding="utf-8"
    )
    assert "ai-governance" in (PROJECT_ROOT / "docs/github_topics.md").read_text(
        encoding="utf-8"
    )
    assert "No AWS resources created" in (
        PROJECT_ROOT / "docs/final_checklist.md"
    ).read_text(encoding="utf-8")


def test_run_all_script_contains_all_major_module_commands() -> None:
    script = PROJECT_ROOT / "scripts/run_all_local.sh"

    assert script.exists()
    text = script.read_text(encoding="utf-8")
    for command in MODULE_COMMANDS:
        assert command in text
