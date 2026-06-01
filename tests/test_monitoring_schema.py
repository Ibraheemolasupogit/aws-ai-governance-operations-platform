import pytest
from pydantic import ValidationError

from ai_governance_platform.monitoring.schema import MonitoringRecord


def valid_monitoring_payload() -> dict:
    return {
        "monitoring_record_id": "MON-999",
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
        "guardrail_violation_count": 1,
        "hallucination_risk_flags": 1,
        "availability_percent": 99.9,
        "monitoring_status": "production_ready",
        "health_status": "healthy",
        "retraining_advisory": "not_required",
        "alert_count": 1,
        "recommended_action": "Continue standard monitoring.",
    }


def test_monitoring_record_validates() -> None:
    record = MonitoringRecord.model_validate(valid_monitoring_payload())

    assert record.monitoring_record_id == "MON-999"
    assert record.health_status == "healthy"


def test_quality_above_one_fails_validation() -> None:
    payload = valid_monitoring_payload()
    payload["quality_score"] = 1.2

    with pytest.raises(ValidationError):
        MonitoringRecord.model_validate(payload)
