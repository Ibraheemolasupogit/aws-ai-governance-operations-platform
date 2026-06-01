"""Schemas for local model card artifacts."""

from datetime import date

from pydantic import BaseModel, Field


class ModelCard(BaseModel):
    """Portfolio-ready model card for one AI system."""

    model_card_id: str = Field(min_length=3)
    system_id: str = Field(min_length=3)
    system_name: str = Field(min_length=3)
    system_type: str = Field(min_length=3)
    model_family: str = Field(min_length=2)
    owner: str = Field(min_length=2)
    business_unit: str = Field(min_length=2)
    business_use_case: str = Field(min_length=5)
    intended_users: str = Field(min_length=3)
    intended_use: str = Field(min_length=3)
    out_of_scope_use: str = Field(min_length=3)
    data_sensitivity: str = Field(min_length=3)
    input_data_type: str = Field(min_length=2)
    output_type: str = Field(min_length=2)
    evaluation_summary: str = Field(min_length=3)
    known_limitations: str = Field(min_length=3)
    responsible_ai_considerations: str = Field(min_length=3)
    monitoring_approach: str = Field(min_length=3)
    risk_controls: str = Field(min_length=3)
    approval_status: str = Field(min_length=3)
    risk_rating: str = Field(min_length=3)
    model_card_status: str = Field(min_length=3)
    last_review_date: date
    next_review_date: date
