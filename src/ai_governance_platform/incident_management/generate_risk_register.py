"""Generate local AI risk register records."""

# ruff: noqa: E501

from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records
from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events
from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records
from ai_governance_platform.incident_management.remediation import (
    assign_incident_priority,
    derive_review_frequency,
    next_review_date_for_rating,
    recommend_risk_mitigation,
)
from ai_governance_platform.incident_management.risk_register_schema import RiskRegisterRecord
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.monitoring.generate_monitoring import generate_sample_monitoring_records
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.risk_scoring.scoring import score_inventory


def _control_status(rating: str) -> str:
    return {
        "critical": "ineffective",
        "high": "partially_effective",
        "medium": "partially_effective",
        "low": "effective",
    }[rating]


def _likelihood(rating: str) -> str:
    return {"critical": "likely", "high": "possible", "medium": "possible", "low": "unlikely"}[rating]


def _impact(rating: str) -> str:
    return {"critical": "severe", "high": "high", "medium": "medium", "low": "low"}[rating]


def _risk(
    index: int,
    system,
    category: str,
    residual: str,
    description: str,
    evidence: str,
) -> RiskRegisterRecord:
    inherent = "critical" if system.risk_tier == "critical" else "high" if residual in {"high", "critical"} else system.risk_tier
    return RiskRegisterRecord(
        risk_id=f"RISK-{index:03d}",
        system_id=system.system_id,
        system_name=system.system_name,
        risk_category=category,
        risk_description=description,
        inherent_risk_rating=inherent,
        residual_risk_rating=residual,
        likelihood=_likelihood(residual),
        impact=_impact(residual),
        priority=assign_incident_priority(residual),
        owner=system.owner,
        business_unit=system.business_unit,
        control_status=_control_status(residual),
        control_gap=description,
        evidence_reference=evidence,
        mitigation_plan=recommend_risk_mitigation(category, residual),
        review_frequency=derive_review_frequency(residual),
        next_review_date=next_review_date_for_rating(residual),
        status="mitigating" if residual in {"high", "critical"} else "monitoring",
    )


def generate_risk_register() -> list[RiskRegisterRecord]:
    """Generate deterministic risk register entries from local synthetic outputs."""
    inventory = generate_sample_inventory()
    systems = {record.system_id: record for record in inventory}
    policies = run_policy_checks(inventory)
    access = review_access_records(generate_sample_access_records())
    costs = generate_sample_cost_records()
    monitoring = generate_sample_monitoring_records()
    audits = generate_sample_audit_events()
    scores = score_inventory(inventory, policies)
    risks: list[RiskRegisterRecord] = []

    def add(system_id: str, category: str, residual: str, desc: str, evidence: str) -> None:
        risks.append(_risk(len(risks) + 1, systems[system_id], category, residual, desc, evidence))

    for score in scores:
        if score.risk_rating in {"high", "critical"}:
            add(score.system_id, "governance", score.risk_rating, f"Overall governance risk is {score.risk_rating}.", f"outputs/risk_scores.json#{score.system_id}")

    for finding in policies:
        if finding.check_status in {"fail", "warning"}:
            add(finding.system_id, "governance", "high" if finding.check_status == "fail" else "medium", finding.finding, f"outputs/governance_findings.json#{finding.system_id}/{finding.policy_name}")

    for record in access:
        if record.finding_status in {"fail", "warning"}:
            add(record.system_id, "access_control", "high" if record.finding_status == "fail" else "medium", record.finding_reason, f"outputs/access_review.json#{record.access_id}")

    for cost in costs:
        if cost.threshold_status == "breached" or cost.anomaly_status != "normal":
            add(cost.system_id, "cost_management", "high" if cost.anomaly_status == "anomaly" else "medium", cost.anomaly_reason, f"outputs/cost_monitoring.json#{cost.cost_record_id}")

    for record in monitoring:
        if record.health_status in {"critical", "degraded"}:
            add(record.system_id, "operational_resilience", "critical" if record.health_status == "critical" else "high", f"Health status is {record.health_status}.", f"outputs/model_monitoring.json#{record.monitoring_record_id}")
        if record.retraining_advisory in {"urgent", "recommended"}:
            add(record.system_id, "model_performance", "critical" if record.retraining_advisory == "urgent" else "high", f"Retraining advisory is {record.retraining_advisory}.", f"outputs/model_monitoring.json#{record.monitoring_record_id}")
        if record.guardrail_violation_count > 0 or record.hallucination_risk_flags > 0:
            add(record.system_id, "responsible_ai", "high" if record.guardrail_violation_count >= 10 else "medium", "Guardrail or hallucination monitoring requires oversight.", f"outputs/model_monitoring.json#{record.monitoring_record_id}")

    for event in audits:
        if event.outcome == "failure":
            add(event.system_id, "auditability", event.severity, event.change_summary, f"outputs/audit_events.json#{event.event_id}")

    for system in inventory:
        if system.data_sensitivity in {"confidential", "restricted"}:
            add(system.system_id, "data_sensitivity", "high" if system.data_sensitivity == "restricted" else "medium", f"System processes {system.data_sensitivity} synthetic data classification.", f"outputs/ai_system_inventory.json#{system.system_id}")

    return risks
