# Model Card: Demand Forecasting Model

## Overview
- System ID: AI-009
- System Type: traditional_ml
- Model Family: time-series-forecasting
- Owner: Grace Morgan
- Business Unit: Supply Chain
- Approval Status: approved
- Risk Rating: medium

## Intended Use
Forecast product demand for inventory planning

## Intended Users
Supply Chain users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: confidential
- Input Data Type: synthetic sales and operations planning features
- Output Type: demand forecast

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.69; drift score 0.72; health status degraded.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: cost_management, data_sensitivity, model_performance, operational_resilience.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: recommended.

## Risk Controls
Risk rating medium; policy gaps: none identified.

## Review
- Model Card Status: complete
- Last Review Date: 2026-05-01
- Next Review Date: 2026-10-28
