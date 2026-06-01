from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.model_cards.generate_model_cards import generate_model_cards


def test_one_model_card_generated_per_inventory_system() -> None:
    assert len(generate_model_cards()) == len(generate_sample_inventory())


def test_model_cards_include_required_content() -> None:
    cards = generate_model_cards()

    assert all(card.owner for card in cards)
    assert all(card.business_use_case for card in cards)
    assert all(card.known_limitations for card in cards)
    assert all(card.monitoring_approach for card in cards)
    assert all(card.risk_controls for card in cards)
    assert all(card.last_review_date and card.next_review_date for card in cards)
