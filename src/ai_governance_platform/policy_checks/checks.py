"""Config-driven governance policy checks for AI system inventory records."""

from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

import yaml

from ai_governance_platform.inventory.schema import AISystemRecord
from ai_governance_platform.policy_checks.schema import PolicyCheckResult

DEFAULT_POLICY_CONFIG_PATH = Path("config/policy_checks.yaml")
VALID_RISK_TIERS = {"low", "medium", "high", "critical"}
PRODUCTION_READY_MONITORING_STATUSES = {"enhanced", "production_ready"}
HIGH_RISK_TIERS = {"high", "critical"}

PolicyRule = dict[str, Any]
PolicyCheckFunction = Callable[[AISystemRecord, PolicyRule], PolicyCheckResult]


def load_policy_config(
    config_path: Path | str = DEFAULT_POLICY_CONFIG_PATH,
) -> dict[str, PolicyRule]:
    """Load policy check configuration from a local YAML file."""
    path = Path(config_path)
    with path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}
    return config.get("rules", {})


def enabled_policy_rules(
    config_path: Path | str = DEFAULT_POLICY_CONFIG_PATH,
) -> dict[str, PolicyRule]:
    """Return enabled policy rules from the configured rule set."""
    rules = load_policy_config(config_path)
    return {name: rule for name, rule in rules.items() if rule.get("enabled", False)}


def _result(
    record: AISystemRecord,
    rule_name: str,
    rule: PolicyRule,
    check_status: str,
    finding: str,
    recommendation: str,
    evidence_field: str,
) -> PolicyCheckResult:
    return PolicyCheckResult(
        system_id=record.system_id,
        system_name=record.system_name,
        policy_name=rule.get("policy_name", rule_name),
        policy_category=rule["category"],
        check_status=check_status,
        severity=rule["severity"],
        finding=finding,
        recommendation=recommendation,
        evidence_field=evidence_field,
    )


def owner_required(record: AISystemRecord, rule: PolicyRule) -> PolicyCheckResult:
    """Check that the system has an accountable owner."""
    has_owner = bool(record.owner and record.owner.strip())
    status = "pass" if has_owner else "fail"
    finding = "AI system has an accountable owner." if has_owner else "AI system owner is missing."
    recommendation = (
        "Keep the owner current during each governance review."
        if has_owner
        else "Assign a named accountable business or technical owner."
    )
    return _result(record, "owner_required", rule, status, finding, recommendation, "owner")


def risk_tier_required(record: AISystemRecord, rule: PolicyRule) -> PolicyCheckResult:
    """Check that the system has a supported risk tier."""
    has_valid_risk_tier = record.risk_tier in VALID_RISK_TIERS
    status = "pass" if has_valid_risk_tier else "fail"
    finding = (
        "AI system has a valid risk tier."
        if has_valid_risk_tier
        else "AI system risk tier is missing or invalid."
    )
    recommendation = (
        "Review the risk tier when system scope or deployment exposure changes."
        if has_valid_risk_tier
        else "Assign one of the approved risk tiers: low, medium, high, or critical."
    )
    return _result(record, "risk_tier_required", rule, status, finding, recommendation, "risk_tier")


def approval_required_for_production(record: AISystemRecord, rule: PolicyRule) -> PolicyCheckResult:
    """Check that production systems have approval."""
    is_production = record.deployment_environment == "production"
    is_approved = record.approval_status == "approved"
    status = "fail" if is_production and not is_approved else "pass"
    finding = (
        "Production AI system has approval."
        if status == "pass"
        else "Production AI system is not approved."
    )
    recommendation = (
        "Keep approval evidence attached to the system record."
        if status == "pass"
        else "Complete approval before production use continues."
    )
    return _result(
        record,
        "approval_required_for_production",
        rule,
        status,
        finding,
        recommendation,
        "approval_status",
    )


def monitoring_required_for_production(
    record: AISystemRecord, rule: PolicyRule
) -> PolicyCheckResult:
    """Check that production systems have sufficient monitoring maturity."""
    is_production = record.deployment_environment == "production"
    has_monitoring = record.monitoring_status in PRODUCTION_READY_MONITORING_STATUSES
    status = "fail" if is_production and not has_monitoring else "pass"
    finding = (
        "Production AI system has sufficient monitoring."
        if status == "pass"
        else "Production AI system does not have enhanced or production-ready monitoring."
    )
    recommendation = (
        "Maintain monitoring evidence and alert ownership."
        if status == "pass"
        else "Enable enhanced or production-ready monitoring before production use continues."
    )
    return _result(
        record,
        "monitoring_required_for_production",
        rule,
        status,
        finding,
        recommendation,
        "monitoring_status",
    )


def model_card_required_for_high_risk(
    record: AISystemRecord, rule: PolicyRule
) -> PolicyCheckResult:
    """Check that high and critical risk systems have model card documentation."""
    is_high_risk = record.risk_tier in HIGH_RISK_TIERS
    if is_high_risk and record.model_card_status == "missing":
        status = "fail"
        finding = "High or critical risk AI system is missing a model card."
        recommendation = "Create a model card before approval or continued governed use."
    elif is_high_risk and record.model_card_status == "draft":
        status = "warning"
        finding = "High or critical risk AI system has only a draft model card."
        recommendation = "Complete the model card before the next governance review."
    else:
        status = "pass"
        finding = "Model card status meets the current governance rule."
        recommendation = "Keep model card evidence current as the system changes."
    return _result(
        record,
        "model_card_required_for_high_risk",
        rule,
        status,
        finding,
        recommendation,
        "model_card_status",
    )


def access_review_required_for_production(
    record: AISystemRecord, rule: PolicyRule
) -> PolicyCheckResult:
    """Check that production systems have completed access reviews."""
    is_production = record.deployment_environment == "production"
    has_completed_access_review = record.access_review_status == "complete"
    status = "fail" if is_production and not has_completed_access_review else "pass"
    finding = (
        "Production AI system has a completed access review."
        if status == "pass"
        else "Production AI system does not have a completed access review."
    )
    recommendation = (
        "Continue periodic access review recertification."
        if status == "pass"
        else "Complete access review for production users, service roles, and operators."
    )
    return _result(
        record,
        "access_review_required_for_production",
        rule,
        status,
        finding,
        recommendation,
        "access_review_status",
    )


def cost_center_required(record: AISystemRecord, rule: PolicyRule) -> PolicyCheckResult:
    """Check that the system maps to an accountable cost center."""
    has_cost_center = bool(record.cost_center and record.cost_center.strip())
    status = "pass" if has_cost_center else "fail"
    finding = (
        "AI system has an assigned cost center."
        if has_cost_center
        else "AI system cost center is missing."
    )
    recommendation = (
        "Review cost center ownership during financial governance reviews."
        if has_cost_center
        else "Assign an accountable cost center for AI platform cost monitoring."
    )
    return _result(
        record,
        "cost_center_required",
        rule,
        status,
        finding,
        recommendation,
        "cost_center",
    )


def incident_process_required_for_high_risk(
    record: AISystemRecord, rule: PolicyRule
) -> PolicyCheckResult:
    """Check that high and critical production systems have an incident process."""
    requires_process = (
        record.risk_tier in HIGH_RISK_TIERS and record.lifecycle_status == "production"
    )
    has_process = record.incident_process_status in {"defined", "tested"}
    status = "fail" if requires_process and not has_process else "pass"
    finding = (
        "Incident process status meets the current governance rule."
        if status == "pass"
        else "High or critical production AI system does not have a defined incident process."
    )
    recommendation = (
        "Test incident response periodically for governed production systems."
        if status == "pass"
        else "Define and record an incident process for this production AI system."
    )
    return _result(
        record,
        "incident_process_required_for_high_risk",
        rule,
        status,
        finding,
        recommendation,
        "incident_process_status",
    )


POLICY_CHECKS: dict[str, PolicyCheckFunction] = {
    "owner_required": owner_required,
    "risk_tier_required": risk_tier_required,
    "approval_required_for_production": approval_required_for_production,
    "monitoring_required_for_production": monitoring_required_for_production,
    "model_card_required_for_high_risk": model_card_required_for_high_risk,
    "access_review_required_for_production": access_review_required_for_production,
    "cost_center_required": cost_center_required,
    "incident_process_required_for_high_risk": incident_process_required_for_high_risk,
}


def run_policy_checks(
    inventory: Iterable[AISystemRecord],
    config_path: Path | str = DEFAULT_POLICY_CONFIG_PATH,
) -> list[PolicyCheckResult]:
    """Run all enabled policy checks against inventory records."""
    rules = enabled_policy_rules(config_path)
    results: list[PolicyCheckResult] = []

    for record in inventory:
        for rule_name, rule in rules.items():
            check = POLICY_CHECKS.get(rule_name)
            if check is None:
                continue
            results.append(check(record, rule))

    return results
