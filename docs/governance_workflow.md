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

## Current Milestone

Milestone 4 implements local risk scoring against synthetic inventory and policy findings. No AWS services are connected, and no real data is used.
