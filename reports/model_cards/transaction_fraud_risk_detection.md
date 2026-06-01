# Model Card: Transaction Fraud Risk Detection

## Overview
- System ID: AI-004
- System Type: traditional_ml
- Model Family: ensemble-risk-model
- Owner: Ethan Brooks
- Business Unit: Risk Management
- Approval Status: approved
- Risk Rating: high

## Intended Use
Identify potentially fraudulent transaction patterns

## Intended Users
Risk Management users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: restricted
- Input Data Type: transaction and account behavior features
- Output Type: fraud risk score

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.88; drift score 0.42; health status watch.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: access_control, auditability, cost_management, data_sensitivity, governance.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: monitor.

## Risk Controls
Risk rating high; policy gaps: access_review_required_for_production, incident_process_required_for_high_risk.

## Review
- Model Card Status: complete
- Last Review Date: 2026-02-04
- Next Review Date: 2026-08-03
