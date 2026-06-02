from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"

REQUIRED_DOCS = [
    "aws_architecture.md",
    "aws_service_mapping.md",
    "operational_workflow.md",
    "evidence_flow.md",
    "aws_implementation_roadmap.md",
    "architecture_diagram.md",
]

MERMAID_DOCS = [
    "aws_architecture.md",
    "operational_workflow.md",
    "evidence_flow.md",
    "architecture_diagram.md",
]

KEY_SERVICES = [
    "IAM",
    "AWS Organizations",
    "CloudTrail",
    "CloudWatch",
    "AWS Config",
    "S3",
    "SageMaker Model Registry",
    "Bedrock",
    "Budgets",
    "Cost Explorer",
    "EventBridge",
    "Lambda",
    "DynamoDB",
    "Step Functions",
    "QuickSight",
]


def test_required_architecture_docs_exist() -> None:
    missing = [doc for doc in REQUIRED_DOCS if not (DOCS_DIR / doc).exists()]

    assert missing == []


def test_architecture_docs_contain_mermaid_where_expected() -> None:
    for doc in MERMAID_DOCS:
        text = (DOCS_DIR / doc).read_text(encoding="utf-8")
        assert "```mermaid" in text


def test_docs_state_local_synthetic_no_aws_resources() -> None:
    combined = "\n".join((DOCS_DIR / doc).read_text(encoding="utf-8") for doc in REQUIRED_DOCS)
    lowered = combined.lower()

    assert "local" in lowered
    assert "synthetic" in lowered
    assert "does not" in lowered
    assert "aws resources" in lowered


def test_architecture_docs_mention_key_aws_services() -> None:
    combined = "\n".join((DOCS_DIR / doc).read_text(encoding="utf-8") for doc in REQUIRED_DOCS)

    for service in KEY_SERVICES:
        assert service in combined
