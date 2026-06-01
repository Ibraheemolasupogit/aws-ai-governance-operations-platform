from ai_governance_platform.risk_scoring.run_risk_scoring import run_risk_scoring


def test_risk_scoring_runner_returns_useful_summary() -> None:
    scores, summary = run_risk_scoring()

    assert scores
    assert summary["systems_scored"] == len(scores)
    assert summary["average_overall_risk_score"] > 0
    assert summary["count_by_risk_rating"]
    assert summary["count_by_priority"]
    assert summary["highest_risk_system"]
    assert summary["highest_risk_score"] == max(score.overall_risk_score for score in scores)
    assert summary["csv_path"].endswith("outputs/risk_scores.csv")
    assert summary["json_path"].endswith("outputs/risk_scores.json")
