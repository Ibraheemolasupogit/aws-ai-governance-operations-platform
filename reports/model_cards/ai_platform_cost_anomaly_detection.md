# Model Card: AI Platform Cost Anomaly Detection

## Overview
- System ID: AI-008
- System Type: anomaly_detection
- Model Family: cost-variance-detector
- Owner: Samira Ahmed
- Business Unit: Finance Operations
- Approval Status: approved
- Risk Rating: medium

## Intended Use
Identify unusual spend patterns in AI platform cost categories

## Intended Users
Finance Operations users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: internal
- Input Data Type: synthetic cost and usage aggregates
- Output Type: cost anomaly alert

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.93; drift score 0.25; health status healthy.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: access_control.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: not_required.

## Risk Controls
Risk rating medium; policy gaps: none identified.

## Review
- Model Card Status: complete
- Last Review Date: 2026-04-30
- Next Review Date: 2026-10-27
