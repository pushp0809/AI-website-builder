"""API routes for Employee Benefits Portal."""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from generated_app.models import Benefit, FAQ, EligibilitySubmission, ContactMessage
from generated_app.schemas import (
    BenefitResponse,
    FAQResponse,
    EligibilityRequest,
    EligibilityResponse,
    ContactRequest,
    ContactResponse,
)

router = APIRouter(prefix="/api")


def get_db():
    """Dependency for database session."""
    from generated_app.main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/benefits", response_model=List[BenefitResponse])
async def get_benefits(db: Session = Depends(get_db)):
    """Get all benefits."""
    benefits = db.query(Benefit).all()
    return [b.to_dict() for b in benefits]


@router.get("/faqs", response_model=List[FAQResponse])
async def get_faqs(db: Session = Depends(get_db)):
    """Get all FAQs."""
    faqs = db.query(FAQ).order_by(FAQ.display_order).all()
    return [f.to_dict() for f in faqs]


@router.post("/eligibility", response_model=EligibilityResponse)
async def check_eligibility(
    request: EligibilityRequest,
    db: Session = Depends(get_db),
):
    """Check eligibility for benefits based on employment details."""
    # Simple eligibility logic
    is_eligible = (
        request.employment_type == "full-time" and
        request.hours_per_week >= 30 and
        request.tenure_months >= 3
    )
    
    eligible_benefits = []
    reason = ""
    
    if is_eligible:
        benefits = db.query(Benefit).all()
        eligible_benefits = [b.to_dict() for b in benefits]
        reason = "You are eligible for all benefits."
        
        # Check specific requirements
        for benefit in eligible_benefits[:]:
            req = benefit.get("eligibility_requirements", "").lower()
            if "1 year" in req and request.tenure_months < 12:
                eligible_benefits.remove(benefit)
            elif "6 months" in req and request.tenure_months < 6:
                eligible_benefits.remove(benefit)
    else:
        if request.employment_type != "full-time":
            reason = "Only full-time employees are eligible for benefits."
        elif request.hours_per_week < 30:
            reason = "You must work at least 30 hours per week to be eligible."
        elif request.tenure_months < 3:
            reason = "You must be employed for at least 90 days to be eligible."
    
    # Save submission
    submission = EligibilitySubmission(
        employment_type=request.employment_type,
        hours_per_week=request.hours_per_week,
        tenure_months=request.tenure_months,
        is_eligible=is_eligible,
        eligible_benefits=str([b["id"] for b in eligible_benefits]),
    )
    db.add(submission)
    db.commit()
    
    return EligibilityResponse(
        eligible=is_eligible,
        benefits=eligible_benefits,
        reason=reason,
    )


@router.post("/contact", response_model=ContactResponse)
async def submit_contact(
    request: ContactRequest,
    db: Session = Depends(get_db),
):
    """Submit a contact/support message."""
    # Validate email format
    if "@" not in request.email or "." not in request.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Sanitize inputs (basic XSS prevention)
    name = request.name.replace("<", "&lt;").replace(">", "&gt;")
    subject = request.subject.replace("<", "&lt;").replace(">", "&gt;")
    message = request.message.replace("<", "&lt;").replace(">", "&gt;")
    
    contact_message = ContactMessage(
        name=name,
        email=request.email,
        subject=subject,
        message=message,
    )
    db.add(contact_message)
    db.commit()
    db.refresh(contact_message)
    
    return ContactResponse(
        success=True,
        message_id=contact_message.id,
        message="Your message has been submitted successfully.",
    )


@router.get("/admin/messages")
async def get_messages(db: Session = Depends(get_db)):
    """Get all contact messages (admin endpoint)."""
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return [m.to_dict() for m in messages]
