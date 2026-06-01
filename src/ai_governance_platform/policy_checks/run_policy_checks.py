"""CLI-style runner for local governance policy checks."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory
from ai_governance_platform.inventory.schema import AISystemRecord
from ai_governance_platform.policy_checks.checks import (
    enabled_policy_rules,
    run_policy_checks,
)
from ai_governance_platform.policy_checks.export_findings import export_findings
from ai_governance_platform.policy_checks.schema import PolicyCheckResult


def build_policy_check_summary(
    inventory: list[AISystemRecord],
    findings: list[PolicyCheckResult],
    csv_path: Path,
    json_path: Path,
) -> dict[str, Any]:
    """Build a compact summary for CLI output and tests."""
    status_counts = Counter(finding.check_status for finding in findings)
    high_critical_findings_count = sum(
        1
        for finding in findings
        if finding.check_status in {"fail", "warning"} and finding.severity in {"high", "critical"}
    )
    return {
        "systems_checked": len(inventory),
        "policy_checks_executed": len(findings),
        "total_findings": len(findings),
        "pass_count": status_counts["pass"],
        "warning_count": status_counts["warning"],
        "fail_count": status_counts["fail"],
        "high_critical_findings_count": high_critical_findings_count,
        "csv_path": str(csv_path),
        "json_path": str(json_path),
    }


def run_enabled_policy_checks() -> tuple[list[PolicyCheckResult], dict[str, Any]]:
    """Generate sample inventory, run enabled checks, export findings, and return summary."""
    inventory = generate_sample_inventory()
    findings = run_policy_checks(inventory)
    csv_path, json_path = export_findings(findings)
    summary = build_policy_check_summary(inventory, findings, csv_path, json_path)
    return findings, summary


def main() -> None:
    """Run local governance policy checks and print a concise summary."""
    findings, summary = run_enabled_policy_checks()
    enabled_count = len(enabled_policy_rules())

    print("Governance policy checks completed.")
    print(f"Systems checked: {summary['systems_checked']}")
    print(f"Enabled policies: {enabled_count}")
    print(f"Policy checks executed: {summary['policy_checks_executed']}")
    print(f"Total findings: {summary['total_findings']}")
    print(f"Pass count: {summary['pass_count']}")
    print(f"Warning count: {summary['warning_count']}")
    print(f"Fail count: {summary['fail_count']}")
    print(f"High/critical findings count: {summary['high_critical_findings_count']}")
    print("Output files:")
    print(f"  - CSV: {summary['csv_path']}")
    print(f"  - JSON: {summary['json_path']}")
    if findings:
        print("Governance findings are local synthetic results only.")


if __name__ == "__main__":
    main()
