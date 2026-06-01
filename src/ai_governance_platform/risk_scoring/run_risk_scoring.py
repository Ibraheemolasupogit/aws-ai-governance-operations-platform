"""CLI-style runner for local AI governance risk scoring."""

from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.policy_checks.checks import run_policy_checks
from ai_governance_platform.risk_scoring.export_scores import export_scores
from ai_governance_platform.risk_scoring.schema import RiskScoreResult
from ai_governance_platform.risk_scoring.scoring import score_inventory


def build_risk_scoring_summary(
    scores: list[RiskScoreResult], csv_path: Path, json_path: Path
) -> dict[str, Any]:
    """Build a compact summary for CLI output and tests."""
    rating_counts = Counter(score.risk_rating for score in scores)
    priority_counts = Counter(score.priority for score in scores)
    highest_risk = max(scores, key=lambda score: score.overall_risk_score)
    return {
        "systems_scored": len(scores),
        "average_overall_risk_score": round(mean(score.overall_risk_score for score in scores), 2),
        "count_by_risk_rating": dict(sorted(rating_counts.items())),
        "count_by_priority": dict(sorted(priority_counts.items())),
        "highest_risk_system": highest_risk.system_name,
        "highest_risk_score": highest_risk.overall_risk_score,
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_risk_scoring() -> tuple[list[RiskScoreResult], dict[str, Any]]:
    """Generate inventory, run policy checks, score systems, export scores, and summarize."""
    inventory = generate_sample_inventory()
    findings = run_policy_checks(inventory)
    scores = score_inventory(inventory, findings)
    csv_path, json_path = export_scores(scores)
    summary = build_risk_scoring_summary(scores, csv_path, json_path)
    return scores, summary


def main() -> None:
    """Run local risk scoring and print a concise summary."""
    scores, summary = run_risk_scoring()

    print("AI governance risk scoring completed.")
    print(f"Systems scored: {summary['systems_scored']}")
    print(f"Average overall risk score: {summary['average_overall_risk_score']}")
    print("Count by risk rating:")
    for rating, count in summary["count_by_risk_rating"].items():
        print(f"  - {rating}: {count}")
    print("Count by priority:")
    for priority, count in summary["count_by_priority"].items():
        print(f"  - {priority}: {count}")
    print(
        "Highest risk system: "
        f"{summary['highest_risk_system']} ({summary['highest_risk_score']})"
    )
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if scores:
        print("Risk scores are local synthetic results only.")


if __name__ == "__main__":
    main()
