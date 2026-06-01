"""Generate incident register records from local governance outputs."""

# ruff: noqa: E501

from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records
from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events
from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records
from ai_governance_platform.incident_management.remediation import (
    BASE_DETECTED_DATE,
    assign_incident_priority,
    derive_residual_risk,
    derive_target_resolution_date,
    recommend_incident_action,
)
from ai_governance_platform.incident_management.schema import IncidentRecord
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.monitoring.generate_monitoring import generate_sample_monitoring_records
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.risk_scoring.scoring import score_inventory


def _incident(
    index: int,
    system,
    incident_type: str,
    severity: str,
    source: str,
    description: str,
    evidence_reference: str,
) -> IncidentRecord:
    production = system.deployment_environment == "production"
    return IncidentRecord(
        incident_id=f"INC-{index:03d}",
        system_id=system.system_id,
        system_name=system.system_name,
        incident_type=incident_type,
        severity=severity,
        status="open" if severity in {"critical", "high"} else "investigating",
        priority=assign_incident_priority(severity),
        source=source,
        detected_date=BASE_DETECTED_DATE,
        owner=system.owner,
        business_unit=system.business_unit,
        description=description,
        evidence_reference=evidence_reference,
        recommended_action=recommend_incident_action(incident_type, severity),
        remediation_status="not_started" if severity in {"critical", "high"} else "in_progress",
        target_resolution_date=derive_target_resolution_date(severity, production),
        residual_risk=derive_residual_risk(severity),
    )


def generate_incidents_from_governance_outputs() -> list[IncidentRecord]:
    """Generate deterministic incident records from local synthetic outputs."""
    inventory = generate_sample_inventory()
    systems = {record.system_id: record for record in inventory}
    policy_findings = run_policy_checks(inventory)
    access_records = review_access_records(generate_sample_access_records())
    audit_events = generate_sample_audit_events()
    cost_records = generate_sample_cost_records()
    monitoring_records = generate_sample_monitoring_records()
    risk_scores = score_inventory(inventory, policy_findings)

    incidents: list[IncidentRecord] = []

    def add(system_id: str, incident_type: str, severity: str, source: str, desc: str, ref: str) -> None:
        incidents.append(_incident(len(incidents) + 1, systems[system_id], incident_type, severity, source, desc, ref))

    for finding in policy_findings:
        if finding.check_status == "fail":
            add(
                finding.system_id,
                "policy_failure",
                finding.severity,
                "policy_checks",
                f"Failed policy check: {finding.policy_name}. {finding.finding}",
                f"outputs/governance_findings.json#{finding.system_id}/{finding.policy_name}",
            )

    for access in access_records:
        if access.finding_status == "fail":
            severity = "critical" if access.privileged_access and not access.mfa_enabled else "high"
            add(
                access.system_id,
                "access_violation",
                severity,
                "access_review",
                access.finding_reason,
                f"outputs/access_review.json#{access.access_id}",
            )

    for event in audit_events:
        if event.outcome == "failure" and event.severity in {"high", "critical"}:
            add(
                event.system_id,
                "audit_failure" if event.event_category == "policy_check" else "operational_failure",
                event.severity,
                "audit_events",
                event.change_summary,
                f"outputs/audit_events.json#{event.event_id}",
            )

    for cost in cost_records:
        if cost.threshold_status == "breached" or cost.anomaly_status == "anomaly":
            severity = "high" if cost.anomaly_status == "anomaly" else "medium"
            add(
                cost.system_id,
                "cost_anomaly",
                severity,
                "cost_monitoring",
                f"{cost.threshold_status} cost status. {cost.anomaly_reason}",
                f"outputs/cost_monitoring.json#{cost.cost_record_id}",
            )

    for monitoring in monitoring_records:
        if monitoring.health_status in {"critical", "degraded"}:
            add(
                monitoring.system_id,
                "monitoring_degradation",
                "critical" if monitoring.health_status == "critical" else "high",
                "model_monitoring",
                f"Model/system health is {monitoring.health_status}.",
                f"outputs/model_monitoring.json#{monitoring.monitoring_record_id}",
            )
        if monitoring.retraining_advisory in {"urgent", "recommended"}:
            add(
                monitoring.system_id,
                "drift_alert",
                "critical" if monitoring.retraining_advisory == "urgent" else "high",
                "model_monitoring",
                f"Retraining advisory is {monitoring.retraining_advisory}.",
                f"outputs/model_monitoring.json#{monitoring.monitoring_record_id}",
            )
        if monitoring.guardrail_violation_count >= 10:
            add(
                monitoring.system_id,
                "guardrail_violation",
                "high",
                "model_monitoring",
                f"Guardrail violations reached {monitoring.guardrail_violation_count}.",
                f"outputs/model_monitoring.json#{monitoring.monitoring_record_id}",
            )

    for score in risk_scores:
        if score.risk_rating in {"high", "critical"}:
            add(
                score.system_id,
                "operational_failure",
                "high" if score.risk_rating == "high" else "critical",
                "risk_scoring",
                f"Overall risk rating is {score.risk_rating} with score {score.overall_risk_score}.",
                f"outputs/risk_scores.json#{score.system_id}",
            )

    return incidents
