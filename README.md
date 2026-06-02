# AWS AI Governance Operations Platform

## One-Line Summary

A local-first, AWS-oriented AI Governance & Operations Platform for ML and GenAI systems, covering inventory, governance policy checks, risk scoring, access review, auditability, cost monitoring, model monitoring, incident tracking, model cards, and executive reporting.

## Problem Statement

Organizations adopting ML and GenAI need to know which AI systems exist, who owns them, how risky they are, whether they are approved and monitored, who has access, how much they cost, and whether they can produce credible evidence for audit and governance review.

In real environments, that information is often fragmented across model registries, cloud logs, access systems, spreadsheets, dashboards, ticket queues, cost tools, and policy documents. This project demonstrates how those signals can be organized into a practical governance operations layer.

## Why This Project Matters

AI governance is not only a policy problem. It is an operating model problem. Teams need repeatable controls that connect responsible AI expectations with MLOps, LLMOps, cloud operations, security, auditability, cost management, incident response, and executive reporting.

This repository shows how an AWS-oriented AI governance platform could work before connecting to real cloud services.

## What The Platform Does

The platform generates synthetic local evidence for:

- AI system inventory and model catalogue
- Governance policy checks
- Risk scoring
- IAM-style access review
- CloudTrail-style audit events
- Cost monitoring and threshold checks
- CloudWatch-style model/system monitoring
- Drift, quality, latency, error-rate, and guardrail summaries
- Incident register and model risk register
- Model cards
- Governance report, audit evidence pack, model risk summary, and executive summary

## Architecture Overview

The implemented repository is a local Python package with modular components under `src/ai_governance_platform/`. Each module generates, validates, checks, exports, or reports on synthetic governance data.

The target AWS architecture is documented in:

- `docs/aws_architecture.md`
- `docs/aws_service_mapping.md`
- `docs/operational_workflow.md`
- `docs/evidence_flow.md`
- `docs/aws_implementation_roadmap.md`
- `docs/architecture_diagram.md`

## Local-Only Implementation Note

This project does not connect to AWS, create AWS resources, deploy infrastructure, call AWS APIs, use paid services, or process real data. All data is synthetic and generated locally. The AWS mapping is architecture and portfolio documentation only.

## Core Capabilities

- Inventory: tracks AI systems, ownership, lifecycle, sensitivity, approval, monitoring, access review, cost center, and AWS service mapping.
- Policy checks: evaluates minimum governance controls and exports pass/warning/fail findings.
- Risk scoring: calculates system-level governance risk scores from inventory and findings.
- Access review: simulates IAM-style access records, privileged access, MFA, expiry, service roles, and review findings.
- Audit simulation: generates CloudTrail-style events for model, access, approval, monitoring, policy, risk, and incident activity.
- Cost governance: estimates monthly AI platform costs, threshold breaches, and anomaly indicators.
- Monitoring: simulates CloudWatch-style health, drift, quality, latency, errors, guardrails, and retraining advisories.
- Incident and risk registers: converts findings into accountable remediation and risk records.
- Model cards and reporting: produces readable governance artifacts for portfolio and audit-style review.

## Repository Structure

```text
aws-ai-governance-operations-platform/
├── config/                         # Local YAML configuration and AWS capability mapping
├── data/                           # Placeholder folders for future local synthetic data
├── docs/                           # Architecture, workflow, roadmap, portfolio, and runbook docs
├── outputs/                        # Generated CSV/JSON outputs, ignored by Git
├── policies/                       # Placeholder governance policies
├── reports/                        # Generated Markdown reports, ignored by Git
├── scripts/                        # Local helper scripts
├── src/ai_governance_platform/     # Modular Python package
└── tests/                          # Pytest coverage across modules and docs
```

## Milestone Summary

1. Repository foundation and Python package layout.
2. AI system inventory and model catalogue.
3. Governance policy checks.
4. Risk scoring.
5. Access review and audit event simulation.
6. Cost and monitoring summaries.
7. Incident and risk register.
8. Model cards and evidence pack reporting.
9. AWS architecture documentation and operational workflow.
10. Portfolio polish, runbook, CV/LinkedIn material, and final presentation docs.

## How To Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run tests and linting:

```bash
python3 -m pytest
python3 -m ruff check .
```

Run all local modules:

```bash
bash scripts/run_all_local.sh
```

## Commands By Module

```bash
python3 -m ai_governance_platform.inventory.run_inventory
python3 -m ai_governance_platform.policy_checks.run_policy_checks
python3 -m ai_governance_platform.risk_scoring.run_risk_scoring
python3 -m ai_governance_platform.access_review.run_access_review
python3 -m ai_governance_platform.audit.run_audit_simulation
python3 -m ai_governance_platform.cost_management.run_cost_monitoring
python3 -m ai_governance_platform.monitoring.run_monitoring
python3 -m ai_governance_platform.incident_management.run_incident_register
python3 -m ai_governance_platform.model_cards.run_model_cards
python3 -m ai_governance_platform.reporting.run_reporting
```

## Generated Outputs

Inventory:

- `outputs/ai_system_inventory.csv`
- `outputs/ai_system_inventory.json`

Policy checks:

- `outputs/governance_findings.csv`
- `outputs/governance_findings.json`

Risk scoring:

- `outputs/risk_scores.csv`
- `outputs/risk_scores.json`

Access review:

- `outputs/access_review.csv`
- `outputs/access_review.json`

Audit events:

- `outputs/audit_events.csv`
- `outputs/audit_events.json`

Cost monitoring:

- `outputs/cost_monitoring.csv`
- `outputs/cost_monitoring.json`

Model monitoring:

- `outputs/model_monitoring.csv`
- `outputs/model_monitoring.json`

Incident and risk registers:

- `outputs/incident_register.csv`
- `outputs/incident_register.json`
- `outputs/model_risk_register.csv`
- `outputs/model_risk_register.json`

Model cards and reporting:

- `outputs/model_cards.csv`
- `outputs/model_cards.json`
- `outputs/governance_report_summary.csv`
- `outputs/governance_report_summary.json`

## Reports Generated

- `reports/model_cards/`
- `reports/ai_governance_report.md`
- `reports/audit_evidence_pack.md`
- `reports/model_risk_register.md`
- `reports/executive_summary.md`

## AWS Service Mapping

The design maps local capabilities to AWS services including:

- AWS IAM
- AWS Organizations
- AWS CloudTrail
- Amazon CloudWatch
- AWS Config
- Amazon S3
- Amazon SageMaker Model Registry
- Amazon Bedrock
- AWS Budgets
- AWS Cost Explorer
- Amazon EventBridge
- AWS Lambda
- Amazon DynamoDB
- AWS Step Functions
- Amazon QuickSight

See `docs/aws_service_mapping.md` and `config/aws_architecture_mapping.yaml` for the detailed capability mapping.

## Skills Demonstrated

- Python package design with `src` layout
- Pydantic data validation
- Config-driven governance logic
- Synthetic data generation
- Local CSV/JSON/Markdown reporting
- Pytest coverage
- Ruff linting
- AI governance and responsible AI controls
- MLOps and LLMOps operational thinking
- AWS architecture mapping
- Auditability and evidence design
- Model risk and incident management
- Cost governance and operational monitoring

## Portfolio Positioning

This project demonstrates the governance and operations layer that sits around AI systems once they move beyond experimentation. It is designed to show practical capability across AI governance operations, responsible AI controls, model risk management, MLOps and LLMOps operating practices, auditability, evidence generation, access review, least-privilege governance, cost oversight, model/system monitoring, and AWS-aligned architecture design.

Unlike a model-training demo, this repository focuses on the controls, workflows, evidence, and reporting needed to operate ML and GenAI systems responsibly. The implementation is intentionally local and synthetic so the project can be reviewed, tested, and extended without cloud credentials, cloud spend, or real sensitive data.

Supporting documentation:

- `docs/portfolio_summary.md`
- `docs/aws_architecture.md`
- `docs/operational_workflow.md`
- `docs/evidence_flow.md`
- `docs/runbook.md`

## Future Enhancements

- Add real AWS API ingestion behind explicit configuration.
- Add infrastructure-as-code after security and architecture review.
- Add authenticated dashboards only if useful.
- Add richer evidence pack formats such as PDF.
- Add policy exception workflows and approval history.
- Add multi-account AWS Organizations support.
- Add production-grade logging, observability, and secrets handling.

## Disclaimer

This is a synthetic local portfolio project. It does not create real AWS resources, call AWS APIs, use real customer/model data, or provide production governance assurance. It is designed to demonstrate architecture, implementation discipline, and governance operations thinking.
