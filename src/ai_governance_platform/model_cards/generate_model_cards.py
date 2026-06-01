"""Generate local model cards from synthetic governance data."""

# ruff: noqa: E501

from datetime import timedelta

from ai_governance_platform.incident_management.generate_risk_register import generate_risk_register
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.model_cards.schema import ModelCard
from ai_governance_platform.monitoring.generate_monitoring import generate_sample_monitoring_records
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.risk_scoring.scoring import score_inventory


def generate_model_cards() -> list[ModelCard]:
    """Generate one deterministic model card per AI system."""
    inventory = generate_sample_inventory()
    findings = run_policy_checks(inventory)
    scores = {score.system_id: score for score in score_inventory(inventory, findings)}
    monitoring = {record.system_id: record for record in generate_sample_monitoring_records()}
    risks_by_system: dict[str, list[str]] = {}
    for risk in generate_risk_register():
        risks_by_system.setdefault(risk.system_id, []).append(risk.risk_category)

    cards = []
    for index, system in enumerate(inventory, 1):
        score = scores[system.system_id]
        monitor = monitoring[system.system_id]
        failed_findings = [
            finding.policy_name
            for finding in findings
            if finding.system_id == system.system_id and finding.check_status != "pass"
        ]
        risk_categories = sorted(set(risks_by_system.get(system.system_id, [])))
        next_review = system.last_review_date + timedelta(days=180)
        cards.append(
            ModelCard(
                model_card_id=f"MC-{index:03d}",
                system_id=system.system_id,
                system_name=system.system_name,
                system_type=system.system_type,
                model_family=system.model_family,
                owner=system.owner,
                business_unit=system.business_unit,
                business_use_case=system.business_use_case,
                intended_users=f"{system.business_unit} users and accountable governance reviewers.",
                intended_use=system.business_use_case,
                out_of_scope_use="Use outside approved business purpose, data scope, or deployment environment is not approved.",
                data_sensitivity=system.data_sensitivity,
                input_data_type=system.input_data_type,
                output_type=system.output_type,
                evaluation_summary=(
                    f"Local synthetic evaluation summary. Quality score {monitor.quality_score}; "
                    f"drift score {monitor.drift_score}; health status {monitor.health_status}."
                ),
                known_limitations=(
                    "Synthetic portfolio artifact; does not represent live model validation, "
                    "real user impact testing, or production AWS telemetry."
                ),
                responsible_ai_considerations=(
                    f"Review data sensitivity, guardrail signals, hallucination flags, and risk categories: "
                    f"{', '.join(risk_categories) or 'standard governance'}."
                ),
                monitoring_approach=(
                    f"Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. "
                    f"Current retraining advisory: {monitor.retraining_advisory}."
                ),
                risk_controls=(
                    f"Risk rating {score.risk_rating}; policy gaps: "
                    f"{', '.join(failed_findings) if failed_findings else 'none identified'}."
                ),
                approval_status=system.approval_status,
                risk_rating=score.risk_rating,
                model_card_status=system.model_card_status,
                last_review_date=system.last_review_date,
                next_review_date=next_review,
            )
        )
    return cards
