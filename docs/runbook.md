# Runbook

## Local-Only Reminder

This repository runs locally with synthetic data. It does not connect to AWS, create AWS resources, call AWS APIs, or use paid services.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Quality Checks

```bash
python3 -m pytest
python3 -m ruff check .
```

## Run Each Module Individually

```bash
python3 -m ai_governance_platform.inventory.run_inventory
python3 -m ai_governance_platform.policy_checks.run_policy_checks
python3 -m ai_governance_platform.risk_scoring.run_risk_scoring
python3 -m ai_governance_platform.access_review.run_access_review
python3 -m ai_governance_platform.audit.run_audit_simulation
python3 -m ai_governance_platform.cost_management.run_cost_monitoring
python3 -m ai_governance_platform.monitoring.run_monitoring
python3 -m ai_governance_platform.incident_management.run_incident_register
python3 -m ai_governance_platform.model_cards.run_model_cards
python3 -m ai_governance_platform.reporting.run_reporting
```

## Suggested Full Manual Execution Order

1. Inventory
2. Policy checks
3. Risk scoring
4. Access review
5. Audit simulation
6. Cost monitoring
7. Model/system monitoring
8. Incident and risk register
9. Model cards
10. Reporting

Run the full sequence with:

```bash
bash scripts/run_all_local.sh
```

## Expected Outputs

- `outputs/ai_system_inventory.csv`
- `outputs/ai_system_inventory.json`
- `outputs/governance_findings.csv`
- `outputs/governance_findings.json`
- `outputs/risk_scores.csv`
- `outputs/risk_scores.json`
- `outputs/access_review.csv`
- `outputs/access_review.json`
- `outputs/audit_events.csv`
- `outputs/audit_events.json`
- `outputs/cost_monitoring.csv`
- `outputs/cost_monitoring.json`
- `outputs/model_monitoring.csv`
- `outputs/model_monitoring.json`
- `outputs/incident_register.csv`
- `outputs/incident_register.json`
- `outputs/model_risk_register.csv`
- `outputs/model_risk_register.json`
- `outputs/model_cards.csv`
- `outputs/model_cards.json`
- `outputs/governance_report_summary.csv`
- `outputs/governance_report_summary.json`
- `reports/model_cards/`
- `reports/ai_governance_report.md`
- `reports/audit_evidence_pack.md`
- `reports/model_risk_register.md`
- `reports/executive_summary.md`

## Troubleshooting

- If module commands fail with `ModuleNotFoundError`, run `pip install -e .`.
- If `pytest` or `ruff` is missing, run `pip install -r requirements.txt`.
- Generated output files are intentionally ignored by Git.
- Markdown reports under `reports/` are generated artifacts and may be regenerated at any time.
