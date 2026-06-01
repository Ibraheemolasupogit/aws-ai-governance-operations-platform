# Governance Workflow

## Overview

The planned workflow will help teams move AI systems from inventory through review, approval, monitoring, and evidence reporting.

## Planned Lifecycle

1. Register AI system metadata.
2. Assign owner, risk tier, status, and environment.
3. Run policy checks.
4. Review access, monitoring, cost, and responsible AI evidence.
5. Record approvals, exceptions, and incidents.
6. Generate audit and executive reports.

## Inventory Foundation

The AI system inventory is the foundation for the future governance workflow. Each local synthetic record captures the ownership, business purpose, lifecycle state, deployment environment, risk tier, data sensitivity, approval status, monitoring status, model card status, access review status, cost center, and planned AWS service mapping needed by later modules.

Future milestones will use this inventory as the input for:

- Governance checks
- Access review
- Risk scoring
- Cost monitoring
- Model cards
- Incident tracking
- Audit evidence reporting

## Policy Findings

Milestone 3 converts each AI inventory record into governance findings by running enabled rules from `config/policy_checks.yaml`. Each rule produces a pass, warning, or fail result with severity, policy category, evidence field, finding text, and a recommendation.

The current policy checks evaluate minimum control readiness across ownership, risk management, production approval, production monitoring, documentation, access control, cost accountability, and incident process readiness. These findings will later become inputs to risk scoring, exception tracking, audit evidence packs, and executive reporting.

## Risk Scoring

Milestone 4 turns inventory and policy findings into system-level risk scores. The scoring engine uses three local inputs:

- AI inventory attributes such as risk tier, lifecycle status, deployment environment, data sensitivity, monitoring status, access review status, approval status, model card status, cost center, and incident process status
- Governance policy findings, especially failed and warning results
- Configurable weights and lookup values from `config/risk_scoring.yaml`

Each system receives component scores, an overall 0-100 score, a risk rating, a remediation priority, and a recommended action. These scores will support later risk registers, access review prioritisation, audit evidence reporting, incident workflows, and executive summaries.

## Access Review And Audit Evidence

Milestone 5 adds synthetic access review and audit event evidence. Access review supports least privilege governance by identifying privileged access, production admin access, expired access, weak service role justification, stale production reviews, and owner access that should be tightly controlled.

Synthetic audit events support traceability by recording model registrations, approvals, deployments, prompt updates, guardrail changes, access grants and revocations, monitoring alerts, policy checks, risk scoring, incident creation, and remediation completion.

Together, these outputs provide local evidence that will feed future incident registers, audit evidence packs, access remediation tracking, and executive reporting.

## Cost And Monitoring Evidence

Milestone 6 adds synthetic cost and monitoring summaries. Cost monitoring supports financial governance by estimating monthly AI system spend, checking local thresholds, identifying approaching and breached thresholds, and flagging cost anomalies for owner review.

Monitoring summaries support operational governance by tracking CloudWatch-style health indicators such as latency, p95 latency, error rate, drift, quality, availability, guardrail violations, hallucination risk flags, and alert volume. Each system receives a health status, retraining advisory, and recommended action.

These outputs will feed future incident and risk registers, audit evidence reporting, cost governance reviews, and executive summaries.

## Current Milestone

Milestone 6 implements local cost and monitoring summaries. No AWS services are connected, and no real data is used.
