import json

import pandas as pd

from ai_governance_platform.inventory.export_inventory import (
    export_inventory,
    export_inventory_to_csv,
    export_inventory_to_json,
)
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory


def test_export_inventory_to_csv_creates_file(tmp_path) -> None:
    inventory = generate_sample_inventory()
    output_path = tmp_path / "inventory.csv"

    created_path = export_inventory_to_csv(inventory, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = pd.read_csv(output_path)
    assert len(exported) == len(inventory)
    assert "system_id" in exported.columns


def test_export_inventory_to_json_creates_file(tmp_path) -> None:
    inventory = generate_sample_inventory()
    output_path = tmp_path / "inventory.json"

    created_path = export_inventory_to_json(inventory, output_path)

    assert created_path == output_path
    assert output_path.exists()
    exported = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(exported) == len(inventory)
    assert "system_id" in exported[0]


def test_export_inventory_creates_csv_and_json(tmp_path) -> None:
    inventory = generate_sample_inventory()
    csv_path = tmp_path / "inventory.csv"
    json_path = tmp_path / "inventory.json"

    created_csv_path, created_json_path = export_inventory(inventory, csv_path, json_path)

    assert created_csv_path.exists()
    assert created_json_path.exists()
