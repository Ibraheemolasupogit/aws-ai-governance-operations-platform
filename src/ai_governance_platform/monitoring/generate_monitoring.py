"""Generate synthetic CloudWatch-style AI monitoring summaries."""

from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.monitoring.checks import evaluate_monitoring_record
from ai_governance_platform.monitoring.schema import MonitoringRecord


def generate_sample_monitoring_records() -> list[MonitoringRecord]:
    """Return deterministic synthetic monitoring records."""
    metric_profiles = {
        "AI-001": (85000, 420, 980, 0.8, 0.22, 0.91, 4, 2, 99.95, 5),
        "AI-002": (12000, 610, 1450, 1.4, 0.48, 0.82, 0, 0, 99.4, 3),
        "AI-003": (240000, 120, 380, 0.3, 0.18, 0.94, 0, 0, 99.99, 1),
        "AI-004": (320000, 360, 1750, 2.2, 0.42, 0.88, 0, 0, 99.7, 4),
        "AI-005": (61000, 480, 1300, 1.1, 0.68, 0.72, 0, 0, 99.2, 5),
        "AI-006": (18000, 920, 2600, 4.5, 0.55, 0.79, 12, 7, 98.6, 9),
        "AI-007": (4000, 700, 1650, 1.8, 0.36, 0.86, 2, 1, 99.1, 2),
        "AI-008": (21000, 240, 700, 0.6, 0.25, 0.93, 0, 0, 99.8, 1),
        "AI-009": (150000, 540, 2300, 3.6, 0.72, 0.69, 0, 0, 98.9, 8),
        "AI-010": (9000, 1100, 3100, 8.8, 0.89, 0.52, 18, 11, 96.4, 14),
    }
    records = []
    for index, system in enumerate(generate_sample_inventory(), 1):
        (
            volume,
            avg_latency,
            p95_latency,
            error_rate,
            drift,
            quality,
            guardrails,
            hallucinations,
            availability,
            alerts,
        ) = metric_profiles[system.system_id]
        record = MonitoringRecord(
            monitoring_record_id=f"MON-{index:03d}",
            system_id=system.system_id,
            system_name=system.system_name,
            system_type=system.system_type,
            monitoring_period="2026-05",
            deployment_environment=system.deployment_environment,
            prediction_volume=volume,
            average_latency_ms=avg_latency,
            p95_latency_ms=p95_latency,
            error_rate_percent=error_rate,
            drift_score=drift,
            quality_score=quality,
            guardrail_violation_count=guardrails,
            hallucination_risk_flags=hallucinations,
            availability_percent=availability,
            monitoring_status=system.monitoring_status,
            alert_count=alerts,
        )
        records.append(evaluate_monitoring_record(record))
    return records
