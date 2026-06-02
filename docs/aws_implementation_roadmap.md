# AWS Implementation Roadmap

This roadmap is future-looking design documentation. The current repository implements Phase 1 only and remains local, synthetic, and non-provisioning.

## Phase 1: Local MVP, Already Implemented

- Objective: Demonstrate governance logic, outputs, and reporting with synthetic local data.
- AWS services involved: None at runtime.
- Outputs: Local CSV, JSON, Markdown model cards, reports, and tests.
- Risks/considerations: Synthetic data does not prove production integration or control effectiveness.

## Phase 2: AWS Data Lake And Evidence Storage

- Objective: Create durable evidence storage and retention patterns.
- AWS services involved: Amazon S3, AWS KMS, IAM, CloudTrail.
- Outputs: Evidence bucket structure, encryption model, retention design.
- Risks/considerations: Access controls, retention, data classification, and audit integrity.

## Phase 3: AWS API Ingestion

- Objective: Ingest metadata and operational signals from AWS APIs.
- AWS services involved: IAM, Organizations, CloudTrail, CloudWatch, AWS Config, SageMaker Model Registry, Bedrock, Cost Explorer, Budgets.
- Outputs: Normalized inventory, access, audit, monitoring, and cost records.
- Risks/considerations: API permissions, pagination, throttling, cross-account access, and data minimization.

## Phase 4: EventBridge And Lambda Automation

- Objective: Run checks and updates from events and schedules.
- AWS services involved: EventBridge, Lambda, S3, DynamoDB.
- Outputs: Automated governance findings, updated current-state records, evidence snapshots.
- Risks/considerations: Idempotency, retries, event ordering, and observability.

## Phase 5: Step Functions Governance Workflow

- Objective: Add human review, approvals, remediation, and accepted-risk workflows.
- AWS services involved: Step Functions, Lambda, DynamoDB, EventBridge, SNS or email integrations.
- Outputs: Workflow execution records, approval evidence, remediation status.
- Risks/considerations: Segregation of duties, reviewer authorization, escalation paths.

## Phase 6: QuickSight Dashboarding

- Objective: Provide operational and executive dashboards.
- AWS services involved: QuickSight, S3, Athena or DynamoDB exports.
- Outputs: Governance dashboards, risk views, incident trends, cost views.
- Risks/considerations: Row-level security, metric definitions, dashboard ownership.

## Phase 7: Multi-Account Governance With AWS Organizations

- Objective: Scale governance across accounts and organizational units.
- AWS services involved: AWS Organizations, IAM Identity Center, CloudTrail organization trails, AWS Config aggregators.
- Outputs: Multi-account coverage, delegated administration, account-level reporting.
- Risks/considerations: Account onboarding, cross-account roles, organizational exceptions.

## Phase 8: Production Hardening And Security Review

- Objective: Prepare for production use.
- AWS services involved: IAM, KMS, CloudTrail, Config, Security Hub, S3, DynamoDB, CloudWatch.
- Outputs: Threat model, runbooks, least privilege roles, monitoring, backup and recovery, security review.
- Risks/considerations: Compliance requirements, incident response, privacy, resilience, operational ownership.
