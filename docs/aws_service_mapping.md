# AWS Service Mapping

This repository remains local and synthetic. It does not create AWS resources or call AWS APIs. The table below explains how each implemented local capability maps to a future AWS production architecture.

| Local capability | Local module/output | AWS service mapping | Production implementation idea | Governance value |
| --- | --- | --- | --- | --- |
| AI system inventory | `inventory`, `outputs/ai_system_inventory.*` | DynamoDB, S3, AWS Organizations | Store current inventory in DynamoDB and archive snapshots in S3 with account context from Organizations. | Establishes authoritative ownership, lifecycle, and environment records. |
| Model catalogue | `inventory`, `model_cards` | SageMaker Model Registry, Bedrock, S3 | Sync model packages and Bedrock application metadata into governed catalogue records. | Supports model traceability and approval review. |
| Policy checks | `policy_checks`, `outputs/governance_findings.*` | AWS Config, Lambda, EventBridge, S3 | Run control checks on schedules or events and persist findings. | Converts governance requirements into repeatable checks. |
| Risk scoring | `risk_scoring`, `outputs/risk_scores.*` | Lambda, DynamoDB, S3, Step Functions | Score systems from findings and inventory, then store current and historical scores. | Prioritizes remediation and risk review. |
| Access review | `access_review`, `outputs/access_review.*` | IAM, AWS Organizations, CloudTrail | Ingest principals, roles, MFA posture, and account context for periodic review. | Supports least privilege and access recertification. |
| Audit event simulation | `audit`, `outputs/audit_events.*` | CloudTrail, CloudWatch, EventBridge, S3 | Normalize audit and operational events into evidence records. | Provides traceability for governance decisions and model changes. |
| Cost monitoring | `cost_management`, `outputs/cost_monitoring.*` | Budgets, Cost Explorer, CloudWatch, S3 | Map cost and usage signals to AI systems, owners, and thresholds. | Supports financial governance and anomaly review. |
| Model/system monitoring | `monitoring`, `outputs/model_monitoring.*` | CloudWatch, SageMaker Model Monitor, Bedrock, EventBridge | Track latency, errors, drift, quality, guardrails, and alerting signals. | Supports operational readiness and responsible AI oversight. |
| Incident register | `incident_management`, `outputs/incident_register.*` | Step Functions, Lambda, DynamoDB, EventBridge | Open incidents from failed controls and route remediation workflows. | Connects issues to owners, dates, priority, and evidence. |
| Risk register | `incident_management`, `outputs/model_risk_register.*` | DynamoDB, S3, Step Functions, QuickSight | Maintain risk records, mitigation plans, review dates, and dashboard views. | Enables recurring governance and risk committee review. |
| Model cards | `model_cards`, `reports/model_cards/` | SageMaker Model Registry, Bedrock, S3 | Generate cards from model metadata, review records, and monitoring evidence. | Documents intended use, limitations, controls, and risk posture. |
| Governance reports | `reporting`, `reports/ai_governance_report.md` | S3, QuickSight, Step Functions | Publish reports to S3 and expose summary metrics in QuickSight. | Turns technical evidence into review-ready governance material. |
| Evidence pack | `reporting`, `reports/audit_evidence_pack.md` | S3, CloudTrail, CloudWatch, AWS Config | Assemble evidence from logs, findings, and workflow records. | Supports audit readiness and evidence retrieval. |
| Executive summary | `reporting`, `reports/executive_summary.md` | QuickSight, S3 | Publish executive metrics, priorities, and narrative summaries. | Translates AI governance into business-level decisions. |

Key AWS services represented: S3, DynamoDB, SageMaker Model Registry, Bedrock, IAM, AWS Organizations, CloudTrail, CloudWatch, AWS Config, Budgets, Cost Explorer, EventBridge, Lambda, Step Functions, and QuickSight.
