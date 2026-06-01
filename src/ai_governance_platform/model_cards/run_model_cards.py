"""CLI-style runner for model card generation."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.model_cards.export_model_cards import export_model_cards
from ai_governance_platform.model_cards.generate_model_cards import generate_model_cards
from ai_governance_platform.model_cards.schema import ModelCard


def build_model_card_summary(
    cards: list[ModelCard], csv_path: Path, json_path: Path, markdown_paths: list[Path]
) -> dict[str, Any]:
    return {
        "total_model_cards_generated": len(cards),
        "count_by_system_type": dict(sorted(Counter(card.system_type for card in cards).items())),
        "count_by_risk_rating": dict(sorted(Counter(card.risk_rating for card in cards).items())),
        "count_by_approval_status": dict(
            sorted(Counter(card.approval_status for card in cards).items())
        ),
        "csv_path": str(csv_path),
        "json_path": str(json_path),
        "markdown_dir": "reports/model_cards",
        "markdown_file_count": len(markdown_paths),
    }


def run_model_cards() -> tuple[list[ModelCard], dict[str, Any]]:
    cards = generate_model_cards()
    csv_path, json_path, markdown_paths = export_model_cards(cards)
    return cards, build_model_card_summary(cards, csv_path, json_path, markdown_paths)


def main() -> None:
    cards, summary = run_model_cards()
    print("Model card generation completed.")
    print(f"Total model cards generated: {summary['total_model_cards_generated']}")
    print(f"Count by system type: {summary['count_by_system_type']}")
    print(f"Count by risk rating: {summary['count_by_risk_rating']}")
    print(f"Count by approval status: {summary['count_by_approval_status']}")
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    print(f"  - Markdown directory: {summary['markdown_dir']}")
    if cards:
        print("Model cards are local synthetic reporting artifacts only.")


if __name__ == "__main__":
    main()
