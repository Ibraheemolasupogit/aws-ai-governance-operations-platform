from ai_governance_platform.monitoring.generate_monitoring import (
    generate_sample_monitoring_records,
)


def test_generated_monitoring_records_are_non_empty() -> None:
    records = generate_sample_monitoring_records()

    assert records


def test_generated_monitoring_records_include_health_statuses() -> None:
    records = generate_sample_monitoring_records()
    statuses = {record.health_status for record in records}

    assert {"healthy", "watch", "degraded", "critical"}.issubset(statuses)


def test_generated_monitoring_records_include_retraining_advisories() -> None:
    records = generate_sample_monitoring_records()
    advisories = {record.retraining_advisory for record in records}

    assert {"not_required", "monitor", "recommended", "urgent"}.issubset(advisories)


def test_generated_monitoring_records_include_genai_guardrail_fields() -> None:
    records = generate_sample_monitoring_records()
    genai_records = [
        record
        for record in records
        if record.system_type in {"genai_llm", "multimodal_ai"}
    ]

    assert any(record.guardrail_violation_count > 0 for record in genai_records)
    assert any(record.hallucination_risk_flags > 0 for record in genai_records)
