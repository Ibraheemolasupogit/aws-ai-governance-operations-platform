from ai_governance_platform.policy_checks.run_policy_checks import run_enabled_policy_checks


def test_policy_check_runner_returns_useful_summary() -> None:
    findings, summary = run_enabled_policy_checks()

    assert findings
    assert summary["systems_checked"] > 0
    assert summary["policy_checks_executed"] == len(findings)
    assert summary["total_findings"] == len(findings)
    assert summary["pass_count"] > 0
    assert summary["warning_count"] > 0
    assert summary["fail_count"] > 0
    assert summary["high_critical_findings_count"] > 0
    assert summary["csv_path"].endswith("outputs/governance_findings.csv")
    assert summary["json_path"].endswith("outputs/governance_findings.json")
