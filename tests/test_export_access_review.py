import json

import pandas as pd

from ai_governance_platform.access_review.export_access_review import (
    export_access_review,
    export_access_review_to_csv,
    export_access_review_to_json,
)
from ai_governance_platform.access_review.generate_access import generate_sample_access_records
from ai_governance_platform.access_review.review import review_access_records


def test_export_access_review_to_csv_creates_file(tmp_path) -> None:
    records = review_access_records(generate_sample_access_records())
    output_path = tmp_path / "access_review.csv"

    created_path = export_access_review_to_csv(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(records)
    assert "finding_status" in exported.columns


def test_export_access_review_to_json_creates_file(tmp_path) -> None:
    records = review_access_records(generate_sample_access_records())
    output_path = tmp_path / "access_review.json"

    created_path = export_access_review_to_json(records, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(records)
    assert "finding_status" in exported[0]


def test_export_access_review_creates_csv_and_json(tmp_path) -> None:
    records = review_access_records(generate_sample_access_records())
    csv_path = tmp_path / "access_review.csv"
    json_path = tmp_path / "access_review.json"

    created_csv_path, created_json_path = export_access_review(records, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
