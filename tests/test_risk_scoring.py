from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.inventory.schema import AISystemRecord
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.policy_checks.schema import PolicyCheckResult
from ai_governance_platform.risk_scoring.scoring import (
    load_risk_scoring_config,
    monitoring_maturity_score,
    policy_failure_score,
    score_inventory,
)


def make_record(**updates) -> AISystemRecord:
    base = generate_sample_inventory()[0].model_dump(mode="json")
    base.update(updates)
    return AISystemRecord.model_validate(base)


def test_generated_inventory_can_be_scored() -> None:
    inventory = generate_sample_inventory()
    findings = run_policy_checks(inventory)
    scores = score_inventory(inventory, findings)

    assert len(scores) == len(inventory)


def test_all_scores_are_between_zero_and_100() -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))

    for score in scores:
        numeric_scores = [
            score.business_criticality_score,
            score.data_sensitivity_score,
            score.deployment_exposure_score,
            score.access_risk_score,
            score.monitoring_maturity_score,
            score.cost_risk_score,
            score.compliance_gap_score,
            score.policy_failure_score,
            score.overall_risk_score,
        ]
        assert all(0 <= value <= 100 for value in numeric_scores)


def test_all_systems_receive_rating_and_priority() -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))

    assert all(score.risk_rating for score in scores)
    assert all(score.priority for score in scores)


def test_production_systems_have_non_zero_deployment_exposure() -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))
    production_scores = [
        score for score in scores if score.deployment_environment == "production"
    ]

    assert production_scores
    assert all(score.deployment_exposure_score > 0 for score in production_scores)


def test_weak_monitoring_increases_monitoring_risk() -> None:
    config = load_risk_scoring_config()
    weak = make_record(monitoring_status="not_enabled", deployment_environment="production")
    strong = make_record(monitoring_status="production_ready", deployment_environment="production")

    assert monitoring_maturity_score(weak, config) > monitoring_maturity_score(strong, config)


def test_failed_policy_findings_increase_policy_failure_score() -> None:
    config = load_risk_scoring_config()
    record = generate_sample_inventory()[0]
    no_findings_score = policy_failure_score(record, [], config)
    findings = [
        PolicyCheckResult(
            system_id=record.system_id,
            system_name=record.system_name,
            policy_name="approval_required_for_production",
            policy_category="approval",
            check_status="fail",
            severity="critical",
            finding="Production AI system is not approved.",
            recommendation="Complete approval before production use continues.",
            evidence_field="approval_status",
        )
    ]

    assert policy_failure_score(record, findings, config) > no_findings_score


def test_at_least_one_high_or_critical_risk_system_exists() -> None:
    inventory = generate_sample_inventory()
    scores = score_inventory(inventory, run_policy_checks(inventory))

    assert any(score.risk_rating in {"high", "critical"} for score in scores)
