# Model Card: Platform Health Anomaly Detection

## Overview
- System ID: AI-003
- System Type: anomaly_detection
- Model Family: time-series-anomaly-detection
- Owner: Nadia Patel
- Business Unit: Cloud Operations
- Approval Status: approved
- Risk Rating: medium

## Intended Use
Detect unusual system health patterns in platform telemetry

## Intended Users
Cloud Operations users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: internal
- Input Data Type: synthetic infrastructure metrics
- Output Type: anomaly alert classification

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.94; drift score 0.18; health status healthy.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: standard governance.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: not_required.

## Risk Controls
Risk rating medium; policy gaps: none identified.

## Review
- Model Card Status: complete
- Last Review Date: 2026-03-18
- Next Review Date: 2026-09-14
