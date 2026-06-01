import json

import pandas as pd

from ai_governance_platform.model_cards.export_model_cards import export_model_cards
from ai_governance_platform.model_cards.generate_model_cards import generate_model_cards


def test_export_model_cards_creates_csv_json_and_markdown(tmp_path) -> None:
    cards = generate_model_cards()
    csv_path, json_path, markdown_paths = export_model_cards(
        cards,
        tmp_path / "model_cards.csv",
        tmp_path / "model_cards.json",
        tmp_path / "model_cards",
    )

    assert csv_path.exists()
    assert json_path.exists()
    assert len(pd.read_csv(csv_path)) == len(cards)
    assert len(json.loads(json_path.read_text(encoding="utf-8"))) == len(cards)
    assert len(markdown_paths) == len(cards)
    assert all(path.exists() for path in markdown_paths)
