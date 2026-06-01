# Model Card: Talent Acquisition Candidate Assessment Model

## Overview
- System ID: AI-002
- System Type: traditional_ml
- Model Family: gradient-boosted-classifier
- Owner: Oliver Grant
- Business Unit: People Operations
- Approval Status: pending
- Risk Rating: high

## Intended Use
Candidate screening support for recruiting workflows

## Intended Users
People Operations users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: restricted
- Input Data Type: candidate profile and assessment features
- Output Type: candidate suitability score

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.82; drift score 0.48; health status watch.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: cost_management, data_sensitivity, governance.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: monitor.

## Risk Controls
Risk rating high; policy gaps: model_card_required_for_high_risk.

## Review
- Model Card Status: draft
- Last Review Date: 2026-04-22
- Next Review Date: 2026-10-19
