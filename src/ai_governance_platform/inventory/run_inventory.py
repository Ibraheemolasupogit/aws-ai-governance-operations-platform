"""CLI-style runner for generating the local AI system inventory."""

from collections import Counter

from ai_governance_platform.inventory.export_inventory import export_inventory
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory


def _format_counts(title: str, counts: Counter[str]) -> str:
    lines = [f"{title}:"]
    lines.extend(f"  - {key}: {counts[key]}" for key in sorted(counts))
    return "\n".join(lines)


def main() -> None:
    """Generate, validate, export, and summarize the sample inventory."""
    inventory = generate_sample_inventory()
    csv_path, json_path = export_inventory(inventory)

    system_type_counts = Counter(record.system_type for record in inventory)
    risk_tier_counts = Counter(record.risk_tier for record in inventory)

    print("AI system inventory generated successfully.")
    print(f"Systems generated: {len(inventory)}")
    print(_format_counts("Systems by type", system_type_counts))
    print(_format_counts("Systems by risk tier", risk_tier_counts))
    print("Output files:")
    print(f"  - CSV: {csv_path}")
    print(f"  - JSON: {json_path}")


if __name__ == "__main__":
    main()
