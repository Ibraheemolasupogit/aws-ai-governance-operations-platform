"""Deterministic remediation helpers for incidents and risks."""

from datetime import date, timedelta

BASE_DETECTED_DATE = date(2026, 6, 1)


def assign_incident_priority(severity: str) -> str:
    return {
        "critical": "urgent",
        "high": "high",
        "medium": "medium",
        "low": "low",
    }[severity]


def recommend_incident_action(incident_type: str, severity: str) -> str:
    if severity == "critical":
        return "Escalate immediately, assign owner, and track remediation daily."
    actions = {
        "policy_failure": "Remediate failed governance control and attach evidence.",
        "access_violation": "Review access, remove inappropriate permissions, and recertify.",
        "cost_anomaly": "Investigate usage drivers and confirm cost owner action.",
        "monitoring_degradation": "Investigate system health and reliability signals.",
        "drift_alert": "Assess drift impact and prepare retraining or recalibration.",
        "guardrail_violation": "Review guardrail controls and update safety mitigations.",
        "audit_failure": "Restore traceability and document missing evidence.",
        "operational_failure": "Review operational risk and implement corrective action.",
    }
    return actions[incident_type]


def derive_target_resolution_date(severity: str, production: bool = False) -> date:
    days = {"critical": 7, "high": 14, "medium": 30, "low": 60}[severity]
    if production and severity in {"critical", "high"}:
        days = max(3, days - 4)
    return BASE_DETECTED_DATE + timedelta(days=days)


def derive_residual_risk(severity: str, accepted_risk: bool = False) -> str:
    if accepted_risk:
        return severity
    return {
        "critical": "high",
        "high": "medium",
        "medium": "low",
        "low": "low",
    }[severity]


def recommend_risk_mitigation(risk_category: str, risk_rating: str) -> str:
    prefix = "Prioritise remediation" if risk_rating in {"high", "critical"} else "Monitor"
    mitigations = {
        "governance": "governance control gaps and approval evidence.",
        "access_control": "least privilege, MFA, and access recertification.",
        "model_performance": "drift, quality, and retraining controls.",
        "responsible_ai": "guardrails, safety testing, and model card evidence.",
        "cost_management": "threshold ownership and cost anomaly remediation.",
        "operational_resilience": "availability, latency, error rate, and alert response.",
        "auditability": "audit trail completeness and evidence references.",
        "data_sensitivity": "data handling controls for sensitive AI systems.",
    }
    return f"{prefix} for {mitigations[risk_category]}"


def derive_review_frequency(risk_rating: str) -> str:
    return {
        "critical": "monthly",
        "high": "quarterly",
        "medium": "semiannual",
        "low": "annual",
    }[risk_rating]


def next_review_date_for_rating(risk_rating: str) -> date:
    days = {"critical": 30, "high": 90, "medium": 180, "low": 365}[risk_rating]
    return BASE_DETECTED_DATE + timedelta(days=days)
