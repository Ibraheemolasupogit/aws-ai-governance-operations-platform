from ai_governance_platform.monitoring.checks import (
    evaluate_health_status,
    evaluate_retraining_advisory,
)
from ai_governance_platform.monitoring.schema import MonitoringRecord


def make_monitoring_record(**updates) -> MonitoringRecord:
    payload = {
        "monitoring_record_id": "MON-900",
        "system_id": "AI-001",
        "system_name": "Retail GenAI Shopping Assistant",
        "system_type": "genai_llm",
        "monitoring_period": "2026-05",
        "deployment_environment": "production",
        "prediction_volume": 1000,
        "average_latency_ms": 250,
        "p95_latency_ms": 750,
        "error_rate_percent": 0.5,
        "drift_score": 0.2,
        "quality_score": 0.92,
        "guardrail_violation_count": 0,
        "hallucination_risk_flags": 0,
        "availability_percent": 99.9,
        "monitoring_status": "production_ready",
        "alert_count": 1,
    }
    payload.update(updates)
    return MonitoringRecord.model_validate(payload)


def test_critical_health_status_for_severe_error_rate() -> None:
    record = make_monitoring_record(error_rate_percent=9)

    assert evaluate_health_status(record) == "critical"


def test_urgent_retraining_for_severe_drift() -> None:
    record = make_monitoring_record(drift_score=0.9)

    assert evaluate_retraining_advisory(record) == "urgent"


def test_degraded_or_critical_system_exists_in_generated_records() -> None:
    from ai_governance_platform.monitoring.generate_monitoring import (
        generate_sample_monitoring_records,
    )

    records = generate_sample_monitoring_records()

    assert any(record.health_status in {"degraded", "critical"} for record in records)
