# Model Card: Multimodal Product Search

## Overview
- System ID: AI-007
- System Type: multimodal_ai
- Model Family: text-image-embedding-search
- Owner: Hannah Wright
- Business Unit: Digital Commerce
- Approval Status: not_required
- Risk Rating: medium

## Intended Use
Search product catalogue using text and image inputs

## Intended Users
Digital Commerce users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: internal
- Input Data Type: synthetic text queries and product images
- Output Type: matched product results

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.86; drift score 0.36; health status watch.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: responsible_ai.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: not_required.

## Risk Controls
Risk rating medium; policy gaps: none identified.

## Review
- Model Card Status: missing
- Last Review Date: 2026-02-28
- Next Review Date: 2026-08-27
