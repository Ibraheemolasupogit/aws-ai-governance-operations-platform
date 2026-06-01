# Model Card: Customer Support GenAI Chatbot

## Overview
- System ID: AI-006
- System Type: genai_llm
- Model Family: retrieval-augmented-llm
- Owner: Lucas Rivera
- Business Unit: Customer Experience
- Approval Status: pending
- Risk Rating: high

## Intended Use
Draft support responses using approved knowledge articles

## Intended Users
Customer Experience users and accountable governance reviewers.

## Out-of-Scope Use
Use outside approved business purpose, data scope, or deployment environment is not approved.

## Data, Inputs, And Outputs
- Data Sensitivity: confidential
- Input Data Type: support ticket summaries and knowledge base excerpts
- Output Type: draft support response

## Evaluation Summary
Local synthetic evaluation summary. Quality score 0.79; drift score 0.55; health status degraded.

## Known Limitations
Synthetic portfolio artifact; does not represent live model validation, real user impact testing, or production AWS telemetry.

## Responsible AI Considerations
Review data sensitivity, guardrail signals, hallucination flags, and risk categories: auditability, data_sensitivity, governance, operational_resilience, responsible_ai.

## Monitoring Approach
Monitor latency, error rate, drift, quality, guardrails, availability, and alerts. Current retraining advisory: monitor.

## Risk Controls
Risk rating high; policy gaps: model_card_required_for_high_risk.

## Review
- Model Card Status: draft
- Last Review Date: 2026-05-12
- Next Review Date: 2026-11-08
