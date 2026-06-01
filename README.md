# AWS AI Governance Operations Platform

## One-Line Summary

A local-first, AWS-oriented AI Governance & Operations Platform foundation for governing ML and GenAI systems across inventory, risk, monitoring, auditability, policy review, cost, and reporting workflows.

## Problem Statement

Organizations adopting machine learning and generative AI need a practical way to understand which AI systems exist, who owns them, how risky they are, whether they are monitored, and whether they can produce evidence for audit and governance reviews. In many environments, this information is fragmented across cloud services, spreadsheets, model registries, logs, dashboards, ticket queues, and policy documents.

This repository establishes the foundation for a portfolio-grade platform that will eventually bring those signals together into a lightweight governance and operations layer.

## Why This Project Matters

AI governance is no longer only a policy exercise. Teams need operational controls that connect responsible AI expectations with engineering workflows, cloud operations, cost management, incident response, and executive reporting.

This project is designed to demonstrate how an AWS-oriented platform could support:

- AI system inventory
- Model registry-style catalogue
- Governance policy checks
- Access control review
- CloudTrail-style audit event simulation
- CloudWatch-style system health monitoring
- Cost monitoring
- Drift and quality monitoring summaries
- Guardrail and compliance checks
- Risk scoring
- Incident and risk register
- Model cards
- Audit evidence pack
- Executive reporting

## Target Users

- AI governance and risk teams
- MLOps and LLMOps engineers
- Cloud platform teams
- Security and compliance reviewers
- Data science and machine learning leaders
- Portfolio reviewers assessing applied AWS, AI governance, and operations capability

## Core Capabilities Planned

- Maintain an inventory of ML and GenAI systems, owners, environments, and lifecycle status.
- Track model catalogue metadata similar to a model registry.
- Run local policy checks against governance requirements.
- Review access control posture and ownership accountability.
- Simulate CloudTrail-style audit events with local sample logs.
- Summarize CloudWatch-style health and operational monitoring signals.
- Track cost thresholds and cost risk for AI workloads.
- Summarize drift, quality, and monitoring maturity signals.
- Capture guardrail, compliance, and responsible AI review outcomes.
- Calculate configurable risk scores and risk tiers.
- Maintain incident, issue, and risk register records.
- Generate model card and audit evidence outputs.
- Produce executive-friendly governance and operations reports.

## AWS Services Mapped

This project is local-only for now, but its planned architecture maps to AWS services commonly used in AI governance and operations:

- IAM for identity and access controls
- AWS Organizations for account and organizational structure
- CloudTrail for audit events
- CloudWatch for logs, metrics, alarms, and operational health
- AWS Config for configuration and compliance signals
- S3 for evidence, reports, and metadata storage
- SageMaker Model Registry for model catalogue concepts
- Amazon Bedrock for GenAI workload governance concepts
- AWS Budgets and Cost Explorer for cost tracking
- EventBridge and Lambda for event-driven checks
- DynamoDB for lightweight platform metadata storage
- Step Functions for governance workflow orchestration
- QuickSight for executive reporting concepts

No AWS connections or real AWS resources are created in this milestone.

## Repository Structure

```text
aws-ai-governance-operations-platform/
├── config/                 # Local YAML configuration for governance, risk, policy, cost, and AWS mapping
├── data/                   # Placeholder folders for future local synthetic inputs
├── docs/                   # Architecture, AWS mapping, workflow, and roadmap notes
├── policies/               # Governance and operating policy placeholders
├── reports/                # Generated report outputs, ignored except for .gitkeep
├── outputs/                # Generated data outputs, ignored except for .gitkeep
├── src/ai_governance_platform/
│   ├── access_review/      # Future access review logic
│   ├── audit/              # Future audit event parsing and evidence support
│   ├── cost_management/    # Future cost threshold and cost risk logic
│   ├── incident_management/# Future incident and risk register support
│   ├── inventory/          # Future AI system inventory logic
│   ├── model_cards/        # Future model card generation support
│   ├── monitoring/         # Future health, drift, and quality monitoring summaries
│   ├── policy_checks/      # Future governance rule evaluation
│   ├── reporting/          # Future audit and executive reporting outputs
│   ├── risk_scoring/       # Future configurable risk scoring
│   └── utils/              # Shared local utilities
└── tests/                  # Initial structure and future behavior tests
```

## MVP Roadmap

1. Milestone 1: Repository setup and project foundation.
2. Milestone 2: Local AI system inventory and model catalogue using synthetic sample data.
3. Milestone 3: Config-driven governance policy checks and risk scoring.
4. Milestone 4: Local audit, monitoring, cost, and access review summaries.
5. Milestone 5: Model cards, risk register, incident tracking, and evidence pack generation.
6. Milestone 6: Executive reporting and portfolio-ready documentation.

## Milestone 2: AI System Inventory And Model Catalogue

Milestone 2 adds the first functional local module: a synthetic AI system inventory and model catalogue for ML and GenAI systems. The inventory records capture ownership, business purpose, lifecycle status, deployment environment, risk tier, data sensitivity, approval status, monitoring status, model card status, access review status, cost center, and planned AWS service mapping.

Run the inventory generator locally:

```bash
python3 -m ai_governance_platform.inventory.run_inventory
```

Expected local outputs:

- `outputs/ai_system_inventory.csv`
- `outputs/ai_system_inventory.json`

The generated records are synthetic and are intended to support later governance checks, access review, risk scoring, cost monitoring, model cards, incident tracking, and audit evidence reporting.

## Milestone 3: Governance Policy Checks

Milestone 3 adds a local, config-driven governance policy check engine. It evaluates the synthetic AI inventory against minimum responsible AI operating controls, including ownership, risk tier assignment, production approval, production monitoring readiness, high-risk model card status, production access review completion, cost center assignment, and incident process readiness.

Run the policy checks locally:

```bash
python3 -m ai_governance_platform.policy_checks.run_policy_checks
```

Expected local outputs:

- `outputs/governance_findings.csv`
- `outputs/governance_findings.json`

The findings are generated from local synthetic records only. No AWS services are connected and no real operational data is used.

## Milestone 4: Risk Scoring

Milestone 4 adds local, config-driven AI governance risk scoring. It combines AI system inventory attributes, governance policy findings, and weights from `config/risk_scoring.yaml` to calculate component scores, an overall 0-100 risk score, a risk rating, a remediation priority, and a recommended action for each AI system.

Run the risk scoring locally:

```bash
python3 -m ai_governance_platform.risk_scoring.run_risk_scoring
```

Expected local outputs:

- `outputs/risk_scores.csv`
- `outputs/risk_scores.json`

The risk scores are generated from local synthetic records and local policy findings only. No AWS services are connected and no real operational data is used.

## Milestone 5: Access Review And Audit Event Simulation

Milestone 5 adds local synthetic evidence modules for IAM-style access review and CloudTrail-style audit event simulation. Access review records show who has access to AI systems, whether privileged or production access is risky, and which access records need remediation. Audit events simulate traceable model, access, approval, monitoring, guardrail, policy, risk, and incident activity.

Run the access review locally:

```bash
python3 -m ai_governance_platform.access_review.run_access_review
```

Run the audit simulation locally:

```bash
python3 -m ai_governance_platform.audit.run_audit_simulation
```

Expected local outputs:

- `outputs/access_review.csv`
- `outputs/access_review.json`
- `outputs/audit_events.csv`
- `outputs/audit_events.json`

The access review and audit records are synthetic local evidence only. No IAM, CloudTrail, or AWS APIs are used.

## Milestone 6: Cost And Monitoring Summaries

Milestone 6 adds local synthetic operational telemetry for AI platform cost monitoring and CloudWatch-style model/system monitoring. Cost records estimate monthly Bedrock-style, SageMaker-style, training, inference, and storage costs, then evaluate threshold status and anomaly indicators. Monitoring records summarize latency, error rate, drift, quality, availability, guardrail violations, hallucination risk flags, alert counts, health status, and retraining advisory.

Run cost monitoring locally:

```bash
python3 -m ai_governance_platform.cost_management.run_cost_monitoring
```

Run model/system monitoring locally:

```bash
python3 -m ai_governance_platform.monitoring.run_monitoring
```

Expected local outputs:

- `outputs/cost_monitoring.csv`
- `outputs/cost_monitoring.json`
- `outputs/model_monitoring.csv`
- `outputs/model_monitoring.json`

The cost and monitoring records are synthetic local operational summaries only. No Cost Explorer, Budgets, CloudWatch, Bedrock, SageMaker, or AWS APIs are used.

## Milestone 7: Incident And Risk Register

Milestone 7 consolidates local governance and operations signals into an AI incident register, AI risk register, and remediation tracking outputs. Incidents and risks are derived from policy findings, access review issues, audit events, cost anomalies, monitoring degradation, drift indicators, guardrail signals, and risk scores.

Run incident and risk register generation locally:

```bash
python3 -m ai_governance_platform.incident_management.run_incident_register
```

Expected local outputs:

- `outputs/incident_register.csv`
- `outputs/incident_register.json`
- `outputs/model_risk_register.csv`
- `outputs/model_risk_register.json`

The registers are generated from synthetic local data only and are intended to demonstrate governance operations ownership, prioritisation, remediation, and evidence traceability.

## Current Status

Milestone 7 is complete. The repository contains synthetic AI inventory, governance policy checks, risk scoring, access review, audit simulation, cost monitoring, model/system monitoring, incident register generation, risk register generation, local exports, and tests across the implemented modules.

The platform does not yet include dashboards, AWS integrations, model card generation, final evidence packs, or executive governance reports.

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

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Portfolio Positioning

This repository is designed as a professional portfolio project showing practical understanding of AWS-oriented AI governance, MLOps, LLMOps, responsible AI operations, risk management, audit readiness, and cloud operating controls.

The project intentionally starts local and lightweight so the architecture, testing discipline, configuration model, and documentation can mature before any cloud integration is introduced.
