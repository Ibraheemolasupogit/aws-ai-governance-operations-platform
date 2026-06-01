"""Generate local Markdown governance reports."""

# ruff: noqa: E501

from collections import Counter
from datetime import datetime

from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records
from ai_governance_platform.audit.generate_audit_events import generate_sample_audit_events
from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records
from ai_governance_platform.incident_management.generate_incidents import (
    generate_incidents_from_governance_outputs,
)
from ai_governance_platform.incident_management.generate_risk_register import generate_risk_register
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.model_cards.generate_model_cards import generate_model_cards
from ai_governance_platform.monitoring.generate_monitoring import generate_sample_monitoring_records
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.reporting.schema import GovernanceReportSummary
from ai_governance_platform.risk_scoring.scoring import score_inventory

GENERATED_AT = datetime(2026, 6, 2, 9, 0, 0)


def _local_data() -> dict:
    inventory = generate_sample_inventory()
    policy_findings = run_policy_checks(inventory)
    risk_scores = score_inventory(inventory, policy_findings)
    access = review_access_records(generate_sample_access_records())
    audits = generate_sample_audit_events()
    costs = generate_sample_cost_records()
    monitoring = generate_sample_monitoring_records()
    incidents = generate_incidents_from_governance_outputs()
    risks = generate_risk_register()
    cards = generate_model_cards()
    return {
        "inventory": inventory,
        "policy_findings": policy_findings,
        "risk_scores": risk_scores,
        "access": access,
        "audits": audits,
        "costs": costs,
        "monitoring": monitoring,
        "incidents": incidents,
        "risks": risks,
        "cards": cards,
    }


def generate_governance_summary() -> GovernanceReportSummary:
    data = _local_data()
    return GovernanceReportSummary(
        report_id="GOV-REPORT-2026-05",
        report_name="AI Governance Operations Summary",
        report_period="2026-05",
        total_ai_systems=len(data["inventory"]),
        production_systems=sum(s.deployment_environment == "production" for s in data["inventory"]),
        high_or_critical_risk_systems=sum(
            s.risk_rating in {"high", "critical"} for s in data["risk_scores"]
        ),
        policy_findings_total=len(data["policy_findings"]),
        policy_failures=sum(f.check_status == "fail" for f in data["policy_findings"]),
        access_review_failures=sum(a.finding_status == "fail" for a in data["access"]),
        audit_events_total=len(data["audits"]),
        cost_threshold_breaches=sum(c.threshold_status == "breached" for c in data["costs"]),
        monitoring_degraded_or_critical=sum(
            m.health_status in {"degraded", "critical"} for m in data["monitoring"]
        ),
        open_incidents=sum(i.status == "open" for i in data["incidents"]),
        high_or_critical_incidents=sum(
            i.severity in {"high", "critical"} for i in data["incidents"]
        ),
        risk_register_entries=len(data["risks"]),
        generated_at=GENERATED_AT,
    )


def generate_governance_report_markdown() -> str:
    data = _local_data()
    summary = generate_governance_summary()
    ratings = Counter(score.risk_rating for score in data["risk_scores"])
    health = Counter(record.health_status for record in data["monitoring"])
    return f"""# AI Governance Report

## Platform Overview
This local report summarizes synthetic governance and operations evidence for an AWS-oriented AI Governance & Operations Platform.

## Inventory Summary
- Total AI systems: {summary.total_ai_systems}
- Production systems: {summary.production_systems}
- Model cards generated: {len(data["cards"])}

## Policy Check Summary
- Policy findings total: {summary.policy_findings_total}
- Policy failures: {summary.policy_failures}

## Risk Scoring Summary
- High or critical risk systems: {summary.high_or_critical_risk_systems}
- Risk rating distribution: {dict(sorted(ratings.items()))}

## Access Review Summary
- Access review failures: {summary.access_review_failures}

## Audit Activity Summary
- Audit events total: {summary.audit_events_total}

## Cost Monitoring Summary
- Cost threshold breaches: {summary.cost_threshold_breaches}

## Model Monitoring Summary
- Degraded or critical systems: {summary.monitoring_degraded_or_critical}
- Health distribution: {dict(sorted(health.items()))}

## Incident Summary
- Open incidents: {summary.open_incidents}
- High or critical incidents: {summary.high_or_critical_incidents}

## Risk Register Summary
- Risk register entries: {summary.risk_register_entries}

## Recommended Next Actions
- Prioritize high and critical incident remediation.
- Review systems with cost breaches, degraded monitoring, or policy failures.
- Use model cards and evidence outputs for responsible AI review discussions.
"""


def generate_audit_evidence_pack_markdown() -> str:
    data = _local_data()
    sample_events = data["audits"][:5]
    events = "\n".join(
        f"- {event.event_id}: {event.event_name} ({event.outcome}, {event.severity})"
        for event in sample_events
    )
    return f"""# Audit Evidence Pack

## Audit Scope
Synthetic local evidence for AI inventory, governance controls, access review, audit activity, cost monitoring, model monitoring, incidents, and risk registers.

## Evidence Sources
- Inventory records
- Policy findings
- Access review findings
- Synthetic audit events
- Cost monitoring records
- Model monitoring records
- Incident and risk register records

## Governance Controls Covered
Ownership, approval, monitoring, documentation, access control, cost accountability, incident readiness, and risk tracking.

## Sample Audit Events
{events}

## Policy Evidence
Policy checks are generated locally from the synthetic inventory and exported as governance findings.

## Access Evidence
Access review evidence covers privileged access, MFA, production access, expired access, and service role justification.

## Monitoring Evidence
Monitoring evidence covers latency, error rate, drift, quality, guardrails, hallucination flags, availability, and alerts.

## Cost Evidence
Cost evidence covers threshold status, anomalies, and recommended financial governance actions.

## Incident/Risk Evidence
Incident and risk registers connect findings to owners, priorities, remediation actions, and evidence references.

## Limitations
This evidence pack is local and synthetic. It does not include real AWS telemetry, real IAM permissions, real CloudTrail events, or production audit evidence.
"""


def generate_model_risk_summary_markdown() -> str:
    data = _local_data()
    high_scores = [s for s in data["risk_scores"] if s.risk_rating in {"high", "critical"}]
    categories = Counter(risk.risk_category for risk in data["risks"])
    systems = "\n".join(
        f"- {score.system_name}: {score.risk_rating} ({score.overall_risk_score})"
        for score in high_scores
    )
    return f"""# Model Risk Register Summary

## High/Critical Risk Systems
{systems}

## Top Risk Categories
{dict(sorted(categories.items()))}

## Residual Risk Overview
Residual risks are tracked in the model risk register with owner, mitigation plan, review frequency, and evidence reference.

## Mitigation Themes
- Strengthen governance and approval evidence.
- Reduce access control gaps.
- Prioritize monitoring and drift remediation.
- Track responsible AI and guardrail concerns.

## Owner Accountability
Each risk entry includes an accountable owner and business unit for follow-up.
"""


def generate_executive_summary_markdown() -> str:
    summary = generate_governance_summary()
    return f"""# Executive Summary

## Overview
This portfolio platform demonstrates local AI governance operations for ML and GenAI systems without connecting to AWS.

## Key Governance Strengths
- Complete synthetic inventory and model card coverage.
- Config-driven policy checks and risk scoring.
- Access, audit, cost, monitoring, incident, and risk evidence are linked.

## Key Risks
- High or critical risk systems: {summary.high_or_critical_risk_systems}
- Policy failures: {summary.policy_failures}
- Cost threshold breaches: {summary.cost_threshold_breaches}
- High or critical incidents: {summary.high_or_critical_incidents}

## Priority Actions
- Remediate open high and critical incidents.
- Review degraded monitoring and cost breach systems.
- Use risk register entries to drive recurring governance reviews.

## AWS Architecture Relevance
The design maps to AWS governance patterns across IAM, CloudTrail, CloudWatch, SageMaker Model Registry, Bedrock, Budgets, Cost Explorer, S3, EventBridge, Lambda, Step Functions, and QuickSight concepts.
"""
