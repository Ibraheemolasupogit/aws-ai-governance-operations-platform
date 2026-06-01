from ai_governance_platform.cost_management.generate_costs import generate_sample_cost_records


def test_generated_cost_records_are_non_empty() -> None:
    records = generate_sample_cost_records()

    assert records


def test_generated_cost_records_include_threshold_statuses() -> None:
    records = generate_sample_cost_records()
    statuses = {record.threshold_status for record in records}

    assert {"within_threshold", "approaching_threshold", "breached"}.issubset(statuses)


def test_generated_cost_records_include_anomaly_statuses() -> None:
    records = generate_sample_cost_records()
    statuses = {record.anomaly_status for record in records}

    assert {"normal", "advisory", "anomaly"}.issubset(statuses)


def test_generated_cost_records_include_breach_and_anomaly() -> None:
    records = generate_sample_cost_records()

    assert any(record.threshold_status == "breached" for record in records)
    assert any(record.anomaly_status == "anomaly" for record in records)
