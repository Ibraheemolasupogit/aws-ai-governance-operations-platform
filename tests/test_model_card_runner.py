from ai_governance_platform.model_cards.run_model_cards import run_model_cards


def test_model_card_runner_returns_useful_summary() -> None:
    cards, summary = run_model_cards()

    assert cards
    assert summary["total_model_cards_generated"] == len(cards)
    assert summary["count_by_system_type"]
    assert summary["count_by_risk_rating"]
    assert summary["count_by_approval_status"]
    assert summary["csv_path"].endswith("outputs/model_cards.csv")
    assert summary["json_path"].endswith("outputs/model_cards.json")
    assert summary["markdown_file_count"] == len(cards)
