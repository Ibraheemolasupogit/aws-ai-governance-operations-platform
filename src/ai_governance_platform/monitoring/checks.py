"""Local CloudWatch-style monitoring checks."""

from ai_governance_platform.monitoring.schema import MonitoringRecord


def evaluate_health_status(record: MonitoringRecord) -> str:
    """Evaluate system health from availability, latency, error, drift, and quality."""
    if (
        record.availability_percent < 97
        or record.error_rate_percent >= 8
        or record.drift_score >= 0.85
        or record.quality_score < 0.6
    ):
        return "critical"
    if (
        record.p95_latency_ms >= 2500
        or record.error_rate_percent >= 4
        or record.drift_score >= 0.65
        or record.quality_score < 0.75
    ):
        return "degraded"
    if (
        record.p95_latency_ms >= 1500
        or record.error_rate_percent >= 2
        or record.drift_score >= 0.4
        or record.quality_score < 0.85
        or record.guardrail_violation_count > 0
        or record.hallucination_risk_flags > 0
    ):
        return "watch"
    return "healthy"


def evaluate_retraining_advisory(record: MonitoringRecord) -> str:
    """Evaluate retraining need from drift and quality indicators."""
    if record.drift_score >= 0.85 or record.quality_score < 0.6:
        return "urgent"
    if record.drift_score >= 0.65 or record.quality_score < 0.75:
        return "recommended"
    if record.drift_score >= 0.4 or record.quality_score < 0.85:
        return "monitor"
    return "not_required"


def recommend_monitoring_action(health_status: str, retraining_advisory: str) -> str:
    """Recommend an operational monitoring action."""
    if health_status == "critical" or retraining_advisory == "urgent":
        return "Escalate immediately and prepare remediation or retraining plan."
    if health_status == "degraded" or retraining_advisory == "recommended":
        return "Prioritise owner review and investigate drift, quality, or reliability issues."
    if health_status == "watch" or retraining_advisory == "monitor":
        return "Monitor trend and review in the next operating cycle."
    return "Continue standard monitoring."


def evaluate_monitoring_record(record: MonitoringRecord) -> MonitoringRecord:
    """Evaluate monitoring health and retraining advisory for one record."""
    health_status = evaluate_health_status(record)
    retraining_advisory = evaluate_retraining_advisory(record)
    return record.model_copy(
        update={
            "health_status": health_status,
            "retraining_advisory": retraining_advisory,
            "recommended_action": recommend_monitoring_action(
                health_status, retraining_advisory
            ),
        }
    )
