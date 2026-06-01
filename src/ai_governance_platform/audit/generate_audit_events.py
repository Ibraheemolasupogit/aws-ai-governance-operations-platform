"""Generate synthetic CloudTrail-style audit events."""

# ruff: noqa: E501

from ai_governance_platform.audit.schema import AuditEvent
from ai_governance_platform.inventory.generate_inventory import generate_sample_inventory


def generate_sample_audit_events() -> list[AuditEvent]:
    """Return deterministic synthetic audit events for local development."""
    systems = {record.system_id: record for record in generate_sample_inventory()}
    event_specs = [
        ("AI-001", "RegisterModelVersion", "model_update", "synthetic_sagemaker", "success", "low"),
        ("AI-001", "ApproveModelForProduction", "approval_workflow", "synthetic_governance_platform", "success", "medium"),
        ("AI-001", "DeployModelEndpoint", "model_deployment", "synthetic_sagemaker", "success", "medium"),
        ("AI-001", "UpdatePromptTemplate", "model_update", "synthetic_bedrock", "warning", "medium"),
        ("AI-001", "UpdateBedrockGuardrail", "guardrail_change", "synthetic_bedrock", "success", "high"),
        ("AI-002", "SubmitApprovalRequest", "approval_workflow", "synthetic_governance_platform", "warning", "high"),
        ("AI-002", "RunBiasReview", "policy_check", "synthetic_governance_platform", "warning", "high"),
        ("AI-002", "GrantReviewerAccess", "access_change", "synthetic_cloudtrail", "success", "medium"),
        ("AI-003", "CreateMonitoringAlarm", "monitoring_alert", "synthetic_cloudwatch", "success", "low"),
        ("AI-003", "AnomalyAlertRaised", "monitoring_alert", "synthetic_cloudwatch", "warning", "medium"),
        ("AI-003", "RunRiskScoring", "risk_scoring", "synthetic_governance_platform", "success", "low"),
        ("AI-004", "RegisterFraudModel", "model_update", "synthetic_sagemaker", "success", "medium"),
        ("AI-004", "GrantProductionAdmin", "access_change", "synthetic_cloudtrail", "warning", "critical"),
        ("AI-004", "AccessReviewOverdue", "policy_check", "synthetic_governance_platform", "failure", "high"),
        ("AI-004", "CreateFraudIncident", "incident_event", "synthetic_governance_platform", "failure", "critical"),
        ("AI-004", "CompleteRemediation", "incident_event", "synthetic_governance_platform", "success", "high"),
        ("AI-005", "RegisterRecommendationModel", "model_update", "synthetic_sagemaker", "success", "low"),
        ("AI-005", "RunPolicyChecks", "policy_check", "synthetic_governance_platform", "success", "low"),
        ("AI-005", "RevokeAnalystAccess", "access_change", "synthetic_cloudtrail", "success", "medium"),
        ("AI-006", "CreateChatbotValidationRun", "model_update", "synthetic_bedrock", "success", "medium"),
        ("AI-006", "PromptSafetyWarning", "guardrail_change", "synthetic_bedrock", "warning", "high"),
        ("AI-006", "MonitoringMissingFinding", "policy_check", "synthetic_governance_platform", "failure", "high"),
        ("AI-007", "CreateMultimodalPrototype", "model_update", "synthetic_bedrock", "success", "low"),
        ("AI-007", "DeveloperAccessGranted", "access_change", "synthetic_cloudtrail", "success", "low"),
        ("AI-007", "GuardrailDraftUpdated", "guardrail_change", "synthetic_bedrock", "success", "medium"),
        ("AI-008", "CostAnomalyDetected", "monitoring_alert", "synthetic_cloudwatch", "warning", "medium"),
        ("AI-008", "BudgetThresholdWarning", "monitoring_alert", "synthetic_cloudwatch", "warning", "medium"),
        ("AI-008", "RunCostRiskScoring", "risk_scoring", "synthetic_governance_platform", "success", "low"),
        ("AI-009", "DeployForecastingModel", "model_deployment", "synthetic_sagemaker", "success", "medium"),
        ("AI-009", "DriftAlertRaised", "monitoring_alert", "synthetic_cloudwatch", "warning", "high"),
        ("AI-009", "ProductionApprovalVerified", "approval_workflow", "synthetic_governance_platform", "success", "medium"),
        ("AI-010", "RunResponsibleAIWorkflow", "policy_check", "synthetic_governance_platform", "success", "medium"),
        ("AI-010", "RiskScoreGenerated", "risk_scoring", "synthetic_governance_platform", "success", "medium"),
        ("AI-010", "IncidentCreatedForEvalFailure", "incident_event", "synthetic_governance_platform", "failure", "high"),
        ("AI-010", "EvaluationRemediationCompleted", "incident_event", "synthetic_governance_platform", "success", "medium"),
        ("AI-001", "CloudTrailAccessLogged", "access_change", "synthetic_cloudtrail", "success", "low"),
    ]
    actor_cycle = [
        ("maya.chen", "user"),
        ("ai-platform-runtime-role", "service_role"),
        ("governance-automation", "automation"),
        ("governance.reviewer", "governance_reviewer"),
    ]

    events = []
    for index, (system_id, name, category, source, outcome, severity) in enumerate(event_specs, 1):
        system = systems[system_id]
        actor, actor_type = actor_cycle[index % len(actor_cycle)]
        environment = (
            "production"
            if system.deployment_environment == "production"
            else "staging"
            if system.deployment_environment == "local"
            else system.deployment_environment
        )
        events.append(
            AuditEvent.model_validate(
                {
                    "event_id": f"EVT-{index:03d}",
                    "event_time": f"2026-05-{(index % 28) + 1:02d}T{(index % 12) + 8:02d}:15:00",
                    "system_id": system_id,
                    "system_name": system.system_name,
                    "event_source": source,
                    "event_name": name,
                    "event_category": category,
                    "actor": actor,
                    "actor_type": actor_type,
                    "environment": environment,
                    "outcome": outcome,
                    "severity": severity,
                    "resource_id": f"{system_id.lower()}-{category.replace('_', '-')}",
                    "change_summary": (
                        f"Synthetic {category.replace('_', ' ')} event for {system.system_name}."
                    ),
                    "evidence_reference": f"outputs/evidence/{system_id.lower()}/{index:03d}.json",
                }
            )
        )
    return events
