"""CLI-style runner for incident and risk register generation."""

from collections import Counter
from pathlib import Path
from typing import Any

from ai_governance_platform.incident_management.export_incidents import export_incidents
from ai_governance_platform.incident_management.export_risk_register import export_risk_register
from ai_governance_platform.incident_management.generate_incidents import (
    generate_incidents_from_governance_outputs,
)
from ai_governance_platform.incident_management.generate_risk_register import (
    generate_risk_register,
)
from ai_governance_platform.incident_management.risk_register_schema import RiskRegisterRecord
from ai_governance_platform.incident_management.schema import IncidentRecord


def build_incident_register_summary(
    incidents: list[IncidentRecord],
    risks: list[RiskRegisterRecord],
    incident_csv: Path,
    incident_json: Path,
    risk_csv: Path,
    risk_json: Path,
) -> dict[str, Any]:
    return {
        "total_incidents": len(incidents),
        "incidents_by_severity": dict(sorted(Counter(i.severity for i in incidents).items())),
        "incidents_by_status": dict(sorted(Counter(i.status for i in incidents).items())),
        "incidents_by_source": dict(sorted(Counter(i.source for i in incidents).items())),
        "high_critical_incident_count": sum(i.severity in {"high", "critical"} for i in incidents),
        "total_risk_register_entries": len(risks),
        "risks_by_category": dict(sorted(Counter(r.risk_category for r in risks).items())),
        "risks_by_residual_risk_rating": dict(
            sorted(Counter(r.residual_risk_rating for r in risks).items())
        ),
        "urgent_remediation_count": sum(i.priority == "urgent" for i in incidents),
        "incident_csv_path": str(incident_csv),
        "incident_json_path": str(incident_json),
        "risk_csv_path": str(risk_csv),
        "risk_json_path": str(risk_json),
    }


def run_incident_register() -> tuple[
    list[IncidentRecord], list[RiskRegisterRecord], dict[str, Any]
]:
    incidents = generate_incidents_from_governance_outputs()
    risks = generate_risk_register()
    incident_csv, incident_json = export_incidents(incidents)
    risk_csv, risk_json = export_risk_register(risks)
    summary = build_incident_register_summary(
        incidents, risks, incident_csv, incident_json, risk_csv, risk_json
    )
    return incidents, risks, summary


def main() -> None:
    incidents, risks, summary = run_incident_register()
    print("Incident and risk register generation completed.")
    print(f"Total incidents: {summary['total_incidents']}")
    print(f"Incidents by severity: {summary['incidents_by_severity']}")
    print(f"Incidents by status: {summary['incidents_by_status']}")
    print(f"Incidents by source: {summary['incidents_by_source']}")
    print(f"High/critical incident count: {summary['high_critical_incident_count']}")
    print(f"Total risk register entries: {summary['total_risk_register_entries']}")
    print(f"Risks by category: {summary['risks_by_category']}")
    print(f"Risks by residual risk rating: {summary['risks_by_residual_risk_rating']}")
    print(f"Urgent remediation count: {summary['urgent_remediation_count']}")
    print("Output files:")
    print(f"  - Incident CSV: {summary['incident_csv_path']}")
    print(f"  - Incident JSON: {summary['incident_json_path']}")
    print(f"  - Risk CSV: {summary['risk_csv_path']}")
    print(f"  - Risk JSON: {summary['risk_json_path']}")
    if incidents and risks:
        print("Incident and risk records are local synthetic results only.")


if __name__ == "__main__":
    main()
