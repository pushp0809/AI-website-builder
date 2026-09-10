"""Pydantic schemas for request/response validation."""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class BenefitResponse(BaseModel):
    """Response schema for benefits."""
    id: int
    name: str
    description: str
    category: str
    eligibility_requirements: Optional[str] = None


class FAQResponse(BaseModel):
    """Response schema for FAQs."""
    id: int
    question: str
    answer: str
    category: str


class EligibilityRequest(BaseModel):
    """Request schema for eligibility check."""
    employment_type: str = Field(..., description="Type of employment")
    hours_per_week: int = Field(..., ge=0, description="Hours worked per week")
    tenure_months: int = Field(..., ge=0, description="Months of employment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employment_type": "full-time",
                "hours_per_week": 40,
                "tenure_months": 6,
            }
        }


class EligibilityResponse(BaseModel):
    """Response schema for eligibility check."""
    eligible: bool
    benefits: List[dict]
    reason: str


class ContactRequest(BaseModel):
    """Request schema for contact form."""
    name: str = Field(..., min_length=1, max_length=200)
    email: str = Field(..., min_length=5, max_length=200)
    subject: str = Field(..., min_length=1, max_length=500)
    message: str = Field(..., min_length=1, max_length=5000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "subject": "Question about benefits",
                "message": "I have a question about my health insurance coverage.",
            }
        }


class ContactResponse(BaseModel):
    """Response schema for contact form submission."""
    success: bool
    message_id: int
    message: str
