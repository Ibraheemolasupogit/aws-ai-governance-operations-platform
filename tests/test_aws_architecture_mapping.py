from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = PROJECT_ROOT / "config/aws_architecture_mapping.yaml"

REQUIRED_FIELDS = {
    "capability_name",
    "local_module",
    "local_outputs",
    "aws_services",
    "production_pattern",
    "governance_purpose",
    "maturity_stage",
}

MAJOR_CAPABILITIES = {
    "AI system inventory",
    "Model catalogue",
    "Policy checks",
    "Risk scoring",
    "Access review",
    "Audit event simulation",
    "Cost monitoring",
    "Model and system monitoring",
    "Incident register",
    "Risk register",
    "Model cards",
    "Governance reports",
    "Evidence pack",
    "Executive summary",
}


def load_mapping() -> dict:
    with MAPPING_PATH.open(encoding="utf-8") as mapping_file:
        return yaml.safe_load(mapping_file)


def test_aws_architecture_mapping_loads_successfully() -> None:
    mapping = load_mapping()

    assert "capability_mappings" in mapping
    assert mapping["capability_mappings"]


def test_mapping_contains_all_major_capabilities() -> None:
    entries = load_mapping()["capability_mappings"]
    capabilities = {entry["capability_name"] for entry in entries}

    assert MAJOR_CAPABILITIES.issubset(capabilities)


def test_mapping_entries_include_required_fields() -> None:
    entries = load_mapping()["capability_mappings"]

    for entry in entries:
        assert REQUIRED_FIELDS.issubset(entry)
        assert entry["local_outputs"]
        assert entry["aws_services"]
