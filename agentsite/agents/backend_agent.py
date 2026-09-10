"""Backend Agent - Creates FastAPI routes and business logic."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class BackendAgent(BaseAgent):
    """Generates FastAPI routes, request validation, error handling, and business logic."""

    name = "BackendAgent"
    role = "Backend Developer"
    system_prompt = """You are an expert Backend Developer AI agent.
Create a complete FastAPI application with:
- Proper routing
- Pydantic models for validation
- Error handling
- Business logic
- No hardcoded secrets

Use parameterized queries only - no raw SQL concatenation."""

    input_artifacts = ["05_api_spec.yaml", "models.py"]
    output_artifacts = []
    allowed_tools = ["file_read", "file_write", "lint"]
    validation_rules = [
        "All endpoints must validate input",
        "No raw SQL queries",
        "Proper error handling",
        "No hardcoded secrets",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute backend generation task."""
        # Generate main FastAPI app
        main_content = self._generate_main_app()
        main_path = self.artifact_store.save("main.py", main_content)

        # Generate routes
        routes_content = self._generate_routes()
        routes_path = self.artifact_store.save("routes.py", routes_content)

        # Generate Pydantic schemas
        schemas_content = self._generate_schemas()
        schemas_path = self.artifact_store.save("schemas.py", schemas_content)

        return {
            "success": True,
            "artifacts": [main_path, routes_path, schemas_path],
            "summary": "Generated FastAPI backend application",
        }

    def _generate_main_app(self) -> str:
        """Generate main FastAPI application."""
        return '''"""FastAPI application for Employee Benefits Portal."""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from routes import router
from seed_data import seed_database

# Configuration from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///generated_app/database.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed database if empty
seed_database(DATABASE_URL)

# FastAPI app
app = FastAPI(
    title="Employee Benefits Portal",
    description="Information portal for employee benefits",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="generated_app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="generated_app/templates")

# Include API routes
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/benefits", response_class=HTMLResponse)
async def benefits_page(request: Request):
    """Benefits overview page."""
    return templates.TemplateResponse("benefits.html", {"request": request})


@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """FAQ page."""
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/eligibility", response_class=HTMLResponse)
async def eligibility_page(request: Request):
    """Eligibility checker page."""
    return templates.TemplateResponse("eligibility.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact form page."""
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin page to view messages."""
    return templates.TemplateResponse("admin.html", {"request": request})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors without exposing details."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    def _generate_routes(self) -> str:
        """Generate API routes."""
        return '''"""API routes for Employee Benefits Portal."""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from models import Benefit, FAQ, EligibilitySubmission, ContactMessage
from schemas import (
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
    from main import SessionLocal
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
'''

    def _generate_schemas(self) -> str:
        """Generate Pydantic schemas."""
        return '''"""Pydantic schemas for request/response validation."""

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
'''
