"""SQLAlchemy ORM models for Employee Benefits Portal."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Benefit(Base):
    """Benefit model representing available employee benefits."""
    
    __tablename__ = "benefits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    eligibility_requirements = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "eligibility_requirements": self.eligibility_requirements,
        }


class FAQ(Base):
    """FAQ model for frequently asked questions."""
    
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
        }


class EligibilitySubmission(Base):
    """Model for eligibility check submissions."""
    
    __tablename__ = "eligibility_submissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employment_type = Column(String(50), nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    tenure_months = Column(Integer, nullable=False)
    is_eligible = Column(Boolean, nullable=False)
    eligible_benefits = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "employment_type": self.employment_type,
            "hours_per_week": self.hours_per_week,
            "tenure_months": self.tenure_months,
            "is_eligible": self.is_eligible,
        }


class ContactMessage(Base):
    """Model for contact/support messages."""
    
    __tablename__ = "contact_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
