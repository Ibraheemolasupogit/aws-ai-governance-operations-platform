"""Export synthetic audit events."""

import json
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from ai_governance_platform.audit.schema import AuditEvent

DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_CSV_PATH = DEFAULT_OUTPUT_DIR / "audit_events.csv"
DEFAULT_JSON_PATH = DEFAULT_OUTPUT_DIR / "audit_events.json"


def _events_to_dicts(events: Iterable[AuditEvent]) -> list[dict]:
    return [event.model_dump(mode="json") for event in events]


def export_audit_events_to_csv(
    events: Iterable[AuditEvent], output_path: Path | str = DEFAULT_CSV_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(_events_to_dicts(events)).to_csv(path, index=False)
    return path


def export_audit_events_to_json(
    events: Iterable[AuditEvent], output_path: Path | str = DEFAULT_JSON_PATH
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_events_to_dicts(events), indent=2), encoding="utf-8")
    return path


def export_audit_events(
    events: Iterable[AuditEvent],
    csv_path: Path | str = DEFAULT_CSV_PATH,
    json_path: Path | str = DEFAULT_JSON_PATH,
) -> tuple[Path, Path]:
    event_list = list(events)
    return (
        export_audit_events_to_csv(event_list, csv_path),
        export_audit_events_to_json(event_list, json_path),
    )
