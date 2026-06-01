# Model Card: Retail GenAI Shopping Assistant

## Overview
- System ID: AI-001
- System Type: genai_llm
- Model Family: foundation-model-rag
- Owner: Maya Chen
- Business Unit: Digital Commerce
- Approval Status: approved
- Risk Rating: high

## Intended Use
Personalized shopping guidance for product discovery

## Intended Users
Digital Commerce users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: confidential
- Input Data Type: customer queries and product catalogue metadata
- Output Type: natural language recommendations

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.91; drift score 0.22; health status watch.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: access_control, cost_management, data_sensitivity, governance, responsible_ai.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: not_required.

## Risk Controls
Risk rating high; policy gaps: none identified.

## Review
- Model Card Status: complete
- Last Review Date: 2026-05-10
- Next Review Date: 2026-11-06
