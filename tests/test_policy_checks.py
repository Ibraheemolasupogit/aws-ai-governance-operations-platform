from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.inventory.schema import AISystemRecord
from ai_governance_platform.policy_checks.checks import (
    enabled_policy_rules,
    owner_required,
    run_policy_checks,
)


def make_record(**updates) -> AISystemRecord:
    base = generate_sample_inventory()[0].model_dump(mode="json")
    base.update(updates)
    return AISystemRecord.model_validate(base)


def result_for(policy_name: str, system_id: str, results):
    return next(
        result
        for result in results
        if result.policy_name == policy_name and result.system_id == system_id
    )


def test_enabled_policy_checks_run_against_generated_inventory() -> None:
    inventory = generate_sample_inventory()
    results = run_policy_checks(inventory)
    enabled_rules = enabled_policy_rules()

    assert len(results) == len(inventory) * len(enabled_rules)
    assert {result.check_status for result in results}.issubset({"pass", "fail", "warning"})


def test_production_systems_require_approval() -> None:
    record = make_record(
        system_id="AI-901",
        deployment_environment="production",
        approval_status="pending",
    )

    results = run_policy_checks([record])

    assert result_for("approval_required_for_production", "AI-901", results).check_status == "fail"


def test_production_systems_require_monitoring() -> None:
    record = make_record(
        system_id="AI-902",
        deployment_environment="production",
        monitoring_status="basic",
    )

    results = run_policy_checks([record])

    assert (
        result_for("monitoring_required_for_production", "AI-902", results).check_status
        == "fail"
    )


def test_high_critical_risk_systems_require_model_cards() -> None:
    record = make_record(
        system_id="AI-903",
        risk_tier="critical",
        model_card_status="missing",
    )

    results = run_policy_checks([record])

    assert result_for("model_card_required_for_high_risk", "AI-903", results).check_status == "fail"


def test_draft_model_card_for_high_risk_system_creates_warning() -> None:
    record = make_record(
        system_id="AI-904",
        risk_tier="high",
        model_card_status="draft",
    )

    results = run_policy_checks([record])

    assert (
        result_for("model_card_required_for_high_risk", "AI-904", results).check_status
        == "warning"
    )


def test_production_systems_require_completed_access_reviews() -> None:
    record = make_record(
        system_id="AI-905",
        deployment_environment="production",
        access_review_status="overdue",
    )

    results = run_policy_checks([record])

    assert (
        result_for("access_review_required_for_production", "AI-905", results).check_status
        == "fail"
    )


def test_missing_owner_creates_failed_finding() -> None:
    record = generate_sample_inventory()[0].model_copy(update={"owner": " "})
    rule = enabled_policy_rules()["owner_required"]

    result = owner_required(record, rule)

    assert result.check_status == "fail"
    assert result.evidence_field == "owner"


def test_high_risk_production_systems_require_incident_process() -> None:
    record = make_record(
        system_id="AI-906",
        risk_tier="high",
        lifecycle_status="production",
        incident_process_status="not_defined",
    )

    results = run_policy_checks([record])

    assert (
        result_for("incident_process_required_for_high_risk", "AI-906", results).check_status
        == "fail"
    )


def test_generated_findings_include_pass_fail_and_warning_statuses() -> None:
    results = run_policy_checks(generate_sample_inventory())
    statuses = {result.check_status for result in results}

    assert {"pass", "fail", "warning"}.issubset(statuses)
