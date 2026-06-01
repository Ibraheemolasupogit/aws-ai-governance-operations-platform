"""Config-driven AI governance risk scoring."""

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from ai_governance_platform.inventory.schema import AISystemRecord
from ai_governance_platform.policy_checks.schema import PolicyCheckResult
from ai_governance_platform.risk_scoring.schema import RiskScoreResult

DEFAULT_RISK_CONFIG_PATH = Path("config/risk_scoring.yaml")
GENAI_SYSTEM_TYPES = {"genai_llm", "multimodal_ai"}
PRODUCTION_ENVIRONMENTS = {"production"}


def load_risk_scoring_config(config_path: Path | str = DEFAULT_RISK_CONFIG_PATH) -> dict[str, Any]:
    """Load risk scoring configuration from a local YAML file."""
    path = Path(config_path)
    with path.open(encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}


def _lookup(config: dict[str, Any], category: str, key: str, default: float = 0) -> float:
    return float(config.get("lookup_scores", {}).get(category, {}).get(key, default))


def _clamp_score(score: float) -> float:
    return round(max(0, min(100, score)), 2)


def business_criticality_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score business criticality from risk tier and lifecycle status."""
    risk_tier_score = _lookup(config, "risk_tier", record.risk_tier)
    lifecycle_score = _lookup(config, "lifecycle_status", record.lifecycle_status)
    return _clamp_score((risk_tier_score * 0.7) + (lifecycle_score * 0.3))


def data_sensitivity_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score risk from data sensitivity."""
    return _clamp_score(_lookup(config, "data_sensitivity", record.data_sensitivity))


def deployment_exposure_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score exposure from deployment environment and lifecycle status."""
    environment_score = _lookup(config, "deployment_environment", record.deployment_environment)
    lifecycle_score = _lookup(config, "lifecycle_status", record.lifecycle_status)
    return _clamp_score((environment_score * 0.75) + (lifecycle_score * 0.25))


def access_risk_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score access risk from access review status and production exposure."""
    review_score = _lookup(config, "access_review_status", record.access_review_status)
    production_penalty = 10 if record.deployment_environment in PRODUCTION_ENVIRONMENTS else 0
    return _clamp_score(review_score + production_penalty)


def monitoring_maturity_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score monitoring risk, with extra penalty for weak production monitoring."""
    monitoring_score = _lookup(config, "monitoring_status", record.monitoring_status)
    weak_production_monitoring = (
        record.deployment_environment == "production"
        and record.monitoring_status not in {"enhanced", "production_ready"}
    )
    production_penalty = 15 if weak_production_monitoring else 0
    return _clamp_score(monitoring_score + production_penalty)


def cost_risk_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score cost risk using local proxy fields."""
    score = 20.0
    if record.system_type in GENAI_SYSTEM_TYPES:
        score += 25
    if record.deployment_environment == "production":
        score += 20
    if not record.cost_center.strip():
        score += 35
    return _clamp_score(score)


def compliance_gap_score(record: AISystemRecord, config: dict[str, Any]) -> float:
    """Score compliance gaps from approval, model card, incident process, and production state."""
    scores = [
        _lookup(config, "approval_status", record.approval_status),
        _lookup(config, "model_card_status", record.model_card_status),
        _lookup(config, "incident_process_status", record.incident_process_status),
    ]
    if record.deployment_environment == "production":
        scores.append(_lookup(config, "deployment_environment", "production"))
    return _clamp_score(sum(scores) / len(scores))


def policy_failure_score(
    record: AISystemRecord,
    findings: Iterable[PolicyCheckResult],
    config: dict[str, Any],
) -> float:
    """Score failed and warning policy findings for one system."""
    relevant_findings = [
        finding
        for finding in findings
        if finding.system_id == record.system_id and finding.check_status in {"fail", "warning"}
    ]
    if not relevant_findings:
        return 0.0

    severity_scores = [
        _lookup(config, "policy_finding_severity", finding.severity)
        for finding in relevant_findings
    ]
    status_multiplier = [
        1.0 if finding.check_status == "fail" else 0.6 for finding in relevant_findings
    ]
    weighted_scores = [
        severity * multiplier
        for severity, multiplier in zip(severity_scores, status_multiplier, strict=True)
    ]
    finding_volume_penalty = min(20, len(relevant_findings) * 5)
    return _clamp_score((sum(weighted_scores) / len(weighted_scores)) + finding_volume_penalty)


def overall_risk_score(component_scores: dict[str, float], config: dict[str, Any]) -> float:
    """Calculate weighted overall risk score on a 0-100 scale."""
    weights = config["scoring_weights"]
    weighted_score = sum(component_scores[name] * float(weight) for name, weight in weights.items())
    total_weight = sum(float(weight) for weight in weights.values())
    return _clamp_score(weighted_score / total_weight)


def risk_rating_for_score(score: float) -> str:
    """Map a numeric risk score to a risk rating."""
    if score <= 24:
        return "low"
    if score <= 49:
        return "medium"
    if score <= 74:
        return "high"
    return "critical"


def priority_for_rating(risk_rating: str) -> str:
    """Map risk rating to remediation priority."""
    return {
        "low": "low",
        "medium": "medium",
        "high": "high",
        "critical": "urgent",
    }[risk_rating]


def recommended_action_for_rating(risk_rating: str) -> str:
    """Return a concise recommended action for a risk rating."""
    return {
        "low": "Continue standard monitoring.",
        "medium": "Review governance gaps in next cycle.",
        "high": "Prioritise remediation and owner review.",
        "critical": "Escalate for immediate governance action.",
    }[risk_rating]


def score_ai_system(
    record: AISystemRecord,
    findings: Iterable[PolicyCheckResult],
    config: dict[str, Any] | None = None,
) -> RiskScoreResult:
    """Calculate a risk score for one AI system."""
    scoring_config = config or load_risk_scoring_config()
    finding_list = list(findings)
    component_scores = {
        "business_criticality": business_criticality_score(record, scoring_config),
        "data_sensitivity": data_sensitivity_score(record, scoring_config),
        "deployment_exposure": deployment_exposure_score(record, scoring_config),
        "access_risk": access_risk_score(record, scoring_config),
        "monitoring_maturity": monitoring_maturity_score(record, scoring_config),
        "cost_risk": cost_risk_score(record, scoring_config),
        "compliance_gaps": compliance_gap_score(record, scoring_config),
        "policy_failures": policy_failure_score(record, finding_list, scoring_config),
    }
    overall_score = overall_risk_score(component_scores, scoring_config)
    risk_rating = risk_rating_for_score(overall_score)

    return RiskScoreResult(
        system_id=record.system_id,
        system_name=record.system_name,
        system_type=record.system_type,
        risk_tier=record.risk_tier,
        deployment_environment=record.deployment_environment,
        business_criticality_score=component_scores["business_criticality"],
        data_sensitivity_score=component_scores["data_sensitivity"],
        deployment_exposure_score=component_scores["deployment_exposure"],
        access_risk_score=component_scores["access_risk"],
        monitoring_maturity_score=component_scores["monitoring_maturity"],
        cost_risk_score=component_scores["cost_risk"],
        compliance_gap_score=component_scores["compliance_gaps"],
        policy_failure_score=component_scores["policy_failures"],
        overall_risk_score=overall_score,
        risk_rating=risk_rating,
        priority=priority_for_rating(risk_rating),
        recommended_action=recommended_action_for_rating(risk_rating),
    )


def score_inventory(
    inventory: Iterable[AISystemRecord],
    findings: Iterable[PolicyCheckResult],
    config_path: Path | str = DEFAULT_RISK_CONFIG_PATH,
) -> list[RiskScoreResult]:
    """Calculate risk scores for an inventory."""
    scoring_config = load_risk_scoring_config(config_path)
    finding_list = list(findings)
    return [score_ai_system(record, finding_list, scoring_config) for record in inventory]
