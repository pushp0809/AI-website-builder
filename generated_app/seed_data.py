"""Seed data script for Employee Benefits Portal.
Uses SYNTHETIC DATA ONLY - no real personal information."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from generated_app.models import Base, Benefit, FAQ, EligibilitySubmission, ContactMessage

# Synthetic benefits data
BENEFITS_DATA = [
    {
        "name": "Health Insurance",
        "description": "Comprehensive medical coverage including doctor visits, hospital stays, and prescription drugs.",
        "category": "Medical",
        "eligibility_requirements": "Full-time employees (30+ hours/week) after 90 days",
    },
    {
        "name": "Dental Insurance",
        "description": "Preventive and basic dental care coverage with network dentists.",
        "category": "Medical",
        "eligibility_requirements": "All employees enrolled in health insurance",
    },
    {
        "name": "401(k) Retirement Plan",
        "description": "Tax-advantaged retirement savings with company match up to 4%.",
        "category": "Retirement",
        "eligibility_requirements": "All employees after 6 months of service",
    },
    {
        "name": "Paid Time Off",
        "description": "Generous PTO allowance starting at 15 days per year.",
        "category": "Time Off",
        "eligibility_requirements": "All full-time employees",
    },
    {
        "name": "Employee Assistance Program",
        "description": "Confidential counseling and support services for employees and family members.",
        "category": "Wellness",
        "eligibility_requirements": "All employees and immediate family",
    },
    {
        "name": "Professional Development",
        "description": "Annual stipend for courses, certifications, and conferences.",
        "category": "Career",
        "eligibility_requirements": "Full-time employees after 1 year",
    },
]

# Synthetic FAQ data
FAQS_DATA = [
    {
        "question": "How do I enroll in health insurance?",
        "answer": "New employees can enroll during their first 30 days or during open enrollment period (Nov 1 - Dec 15). Visit the HR portal or contact HR for assistance.",
        "category": "Enrollment",
    },
    {
        "question": "When does my coverage begin?",
        "answer": "Coverage begins on the first day of the month following your enrollment date. For new hires, this is typically your start date if you enroll within 30 days.",
        "category": "Coverage",
    },
    {
        "question": "Can I add my family to my plan?",
        "answer": "Yes! You can add your spouse and dependent children during open enrollment or within 30 days of a qualifying life event.",
        "category": "Coverage",
    },
    {
        "question": "How do I check my PTO balance?",
        "answer": "Log into the employee portal and navigate to 'My Time Off' to view your current balance and accrual history.",
        "category": "Time Off",
    },
    {
        "question": "What is the company match for 401(k)?",
        "answer": "The company matches 100% of your contributions up to 4% of your eligible compensation. You are eligible to participate after 6 months.",
        "category": "Retirement",
    },
]


def seed_database(db_path: str = "./database.db"):
    """Populate database with synthetic seed data."""
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(Benefit).count() > 0:
            print("Database already seeded.")
            return
        
        # Insert benefits
        for benefit_data in BENEFITS_DATA:
            benefit = Benefit(**benefit_data)
            db.add(benefit)
        
        # Insert FAQs
        for i, faq_data in enumerate(FAQS_DATA):
            faq = FAQ(**faq_data, display_order=i)
            db.add(faq)
        
        db.commit()
        print(f"Seeded {len(BENEFITS_DATA)} benefits and {len(FAQS_DATA)} FAQs.")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
