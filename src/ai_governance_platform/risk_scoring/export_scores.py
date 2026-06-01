"""Export AI governance risk scores."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.risk_scoring.schema import RiskScoreResult

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "risk_scores.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "risk_scores.json"


def _scores_to_dicts(scores: Iterable[RiskScoreResult]) -> list[dict]:
    return [score.model_dump(mode="json") for score in scores]


def export_scores_to_csv(
    scores: Iterable[RiskScoreResult], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    """Export risk scores to CSV and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_scores_to_dicts(scores)).to_csv(path, index=False)
    return path


def export_scores_to_json(
    scores: Iterable[RiskScoreResult], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    """Export risk scores to JSON and return the created path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_scores_to_dicts(scores), indent=2), encoding="utf-8")
    return path


def export_scores(
    scores: Iterable[RiskScoreResult],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    """Export risk scores to CSV and JSON."""
    score_list = list(scores)
    return (
        export_scores_to_csv(score_list, csv_path),
        export_scores_to_json(score_list, json_path),
    )
