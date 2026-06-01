"""Export model cards to CSV, JSON, and Markdown."""

import json
import re
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.model_cards.schema import ModelCard

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_REPORT_DIR = Path("reports/model_cards")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "model_cards.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "model_cards.json"


def _cards_to_dicts(cards: Iterable[ModelCard]) -> list[dict]:
    return [card.model_dump(mode="json") for card in cards]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def model_card_to_markdown(card: ModelCard) -> str:
    return f"""# Model Card: {card.system_name}

## Overview
- System ID: {card.system_id}
- System Type: {card.system_type}
- Model Family: {card.model_family}
- Owner: {card.owner}
- Business Unit: {card.business_unit}
- Approval Status: {card.approval_status}
- Risk Rating: {card.risk_rating}

## Intended Use
{card.intended_use}

## Intended Users
{card.intended_users}

## Out-of-Scope Use
{card.out_of_scope_use}

## Data, Inputs, And Outputs
- Data Sensitivity: {card.data_sensitivity}
- Input Data Type: {card.input_data_type}
- Output Type: {card.output_type}

## Evaluation Summary
{card.evaluation_summary}

## Known Limitations
{card.known_limitations}

## Responsible AI Considerations
{card.responsible_ai_considerations}

## Monitoring Approach
{card.monitoring_approach}

## Risk Controls
{card.risk_controls}

## Review
- Model Card Status: {card.model_card_status}
- Last Review Date: {card.last_review_date}
- Next Review Date: {card.next_review_date}
"""


def export_model_cards_to_csv(
    cards: Iterable[ModelCard], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_cards_to_dicts(cards)).to_csv(path, index=False)
    return path


def export_model_cards_to_json(
    cards: Iterable[ModelCard], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_cards_to_dicts(cards), indent=2), encoding="utf-8")
    return path


def export_model_card_markdown(
    cards: Iterable[ModelCard], output_dir: Path | str = DEFAULT_REPORT_DIR
) -> list[Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    paths = []
    for card in cards:
        path = directory / f"{slugify(card.system_name)}.md"
        path.write_text(model_card_to_markdown(card), encoding="utf-8")
        paths.append(path)
    return paths


def export_model_cards(
    cards: Iterable[ModelCard],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
    markdown_dir: Path | str = DEFAULT_REPORT_DIR,
) -> tuple[Path, Path, list[Path]]:
    card_list = list(cards)
    return (
        export_model_cards_to_csv(card_list, csv_path),
        export_model_cards_to_json(card_list, json_path),
        export_model_card_markdown(card_list, markdown_dir),
    )
