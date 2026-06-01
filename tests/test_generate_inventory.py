from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.inventory.schema import AISystemRecord

VALID_RISK_TIERS = {"low", "medium", "high", "critical"}
VALID_SYSTEM_TYPES = {
    "traditional_ml",
    "genai_llm",
    "multimodal_ai",
    "recommendation_system",
    "anomaly_detection",
}


def test_sample_inventory_returns_valid_non_empty_records() -> None:
    inventory = generate_sample_inventory()

    assert inventory
    assert all(isinstance(record, AISystemRecord) for record in inventory)


def test_generated_inventory_contains_required_fields() -> None:
    inventory = generate_sample_inventory()
    required_fields = set(AISystemRecord.model_fields)

    for record in inventory:
        record_fields = set(record.model_dump())
        assert required_fields.issubset(record_fields)


def test_generated_inventory_uses_valid_risk_tiers_and_system_types() -> None:
    inventory = generate_sample_inventory()

    assert {record.risk_tier for record in inventory}.issubset(VALID_RISK_TIERS)
    assert {record.system_type for record in inventory}.issubset(VALID_SYSTEM_TYPES)


def test_generated_inventory_contains_ml_and_genai_style_systems() -> None:
    inventory = generate_sample_inventory()
    system_types = {record.system_type for record in inventory}

    assert "traditional_ml" in system_types
    assert "genai_llm" in system_types


def test_generated_inventory_contains_high_or_critical_risk_system() -> None:
    inventory = generate_sample_inventory()

    assert any(record.risk_tier in {"high", "critical"} for record in inventory)


def test_generated_inventory_contains_production_system() -> None:
    inventory = generate_sample_inventory()

    assert any(record.lifecycle_status == "production" for record in inventory)
