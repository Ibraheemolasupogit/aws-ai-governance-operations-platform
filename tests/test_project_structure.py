from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_major_project_folders_exist() -> None:
    expected_dirs = [
        "config",
        "data",
        "data/inventory",
        "data/audit_logs",
        "data/cost",
        "data/monitoring",
        "data/sample",
        "docs",
        "policies",
        "outputs",
        "reports",
        "src/ai_governance_platform",
        "tests",
    ]

    missing_dirs = [path for path in expected_dirs if not (PROJECT_ROOT / path).is_dir()]

    assert missing_dirs == []
