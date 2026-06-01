from ai_governance_platform.model_cards.schema import ModelCard


def test_model_card_validates() -> None:
    card = ModelCard(
        model_card_id="MC-999",
        system_id="AI-001",
        system_name="Retail GenAI Shopping Assistant",
        system_type="genai_llm",
        model_family="foundation-model-rag",
        owner="Maya Chen",
        business_unit="Digital Commerce",
        business_use_case="Shopping guidance",
        intended_users="Commerce users",
        intended_use="Support product discovery",
        out_of_scope_use="Unapproved decisions",
        data_sensitivity="confidential",
        input_data_type="queries",
        output_type="recommendations",
        evaluation_summary="Synthetic evaluation summary.",
        known_limitations="Synthetic limitations.",
        responsible_ai_considerations="Review safety controls.",
        monitoring_approach="Monitor quality and drift.",
        risk_controls="Policy and access controls.",
        approval_status="approved",
        risk_rating="high",
        model_card_status="complete",
        last_review_date="2026-01-01",
        next_review_date="2026-06-30",
    )

    assert card.system_id == "AI-001"
