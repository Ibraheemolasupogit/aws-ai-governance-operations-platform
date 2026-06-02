#!/usr/bin/env bash
set -euo pipefail

echo "Running local synthetic AI governance platform modules..."

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

echo "All local synthetic modules completed."
