# Interview Talking Points

## 60-Second Project Pitch

I built a local AWS-oriented AI Governance & Operations Platform that simulates the control layer around ML and GenAI systems. It creates an AI system inventory, runs governance policy checks, calculates risk scores, reviews access, simulates audit events, monitors cost and system health, creates incidents and risk registers, generates model cards, and produces audit and executive reports. Everything is synthetic and local, but the architecture maps to AWS services such as IAM, CloudTrail, CloudWatch, SageMaker Model Registry, Bedrock, S3, DynamoDB, Step Functions, and QuickSight.

## Deeper Technical Explanation

The project is a modular Python package using Pydantic schemas, deterministic synthetic generators, config-driven checks, CSV/JSON exporters, Markdown reporting, pytest, and ruff. Each module produces evidence that feeds later modules, creating an end-to-end governance workflow.

## Architecture Explanation

The local implementation mirrors a future AWS architecture where DynamoDB could hold current state, S3 could hold evidence, CloudTrail and CloudWatch could provide events and metrics, EventBridge and Lambda could trigger checks, Step Functions could manage review workflows, and QuickSight could provide reporting.

## Governance Explanation

The platform connects inventory, ownership, policy checks, risk scoring, access review, monitoring, cost, incidents, risk registers, model cards, and evidence packs into one governance operating model.

## AWS Mapping Explanation

The project does not use AWS at runtime. The AWS mapping is documented as a target architecture showing how each local module could be implemented with AWS services in a production version.

## Testing Explanation

The repository includes tests for schemas, generators, checks, exporters, runners, reports, architecture docs, and final portfolio docs. The tests make sure generated data is non-empty, expected statuses exist, outputs are created, and docs include required content.

## Limitations And Honest Trade-Offs

- It uses synthetic data, not real AWS telemetry.
- It does not provision infrastructure.
- It does not include dashboards.
- It demonstrates architecture and governance logic, not production readiness.

## Future Implementation Path

Add AWS API ingestion, S3 evidence storage, DynamoDB current state, EventBridge/Lambda automation, Step Functions workflows, QuickSight dashboards, multi-account support, and production security controls.

## Likely Interview Questions

### Why did you build this project?

To demonstrate AI governance and platform operations, not just model training. I wanted a project that shows how AI systems are controlled, monitored, audited, and reported.

### What problem does it solve?

It organizes fragmented AI governance signals into one operational workflow for inventory, risk, access, audit, monitoring, cost, incidents, and reporting.

### Why local synthetic data?

It keeps the portfolio safe, reproducible, and free to run without AWS credentials, paid services, or real sensitive data.

### How would this map to real AWS?

Use IAM and Organizations for access/account context, CloudTrail and CloudWatch for evidence, Config for compliance, S3 for evidence storage, DynamoDB for current state, EventBridge/Lambda for automation, Step Functions for review workflows, SageMaker/Bedrock for model metadata, and QuickSight for reporting.

### How does it support AI governance?

It enforces ownership, approval, monitoring, documentation, access review, incident readiness, risk scoring, model cards, and evidence packs.

### How does it support model risk management?

It assigns risk scores, records residual risks, tracks mitigation plans, links evidence, and creates review dates and priorities.

### How does it support MLOps/LLMOps?

It adds the operational governance layer around deployments: monitoring, guardrails, cost, audit events, access, incidents, and reporting.

### How do policy checks, risk scoring, and incidents connect?

Policy checks create findings. Findings influence risk scores. Failed or severe findings can create incidents and risk register entries.

### How would you productionise it?

Add AWS ingestion, infrastructure-as-code, secure storage, IAM least privilege, workflow automation, observability, dashboards, and formal security review.

### What would you improve next?

I would add real AWS data ingestion behind optional configuration, then build a dashboard or API only after the evidence model is stable.
