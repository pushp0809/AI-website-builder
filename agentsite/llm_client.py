"""Unified LLM client supporting MockLLM and RealLLM."""

import json
import os
from abc import ABC, abstractmethod
from typing import Any

from agentsite.config import settings


class BaseLLM(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system_prompt: str = "") -> dict[str, Any]:
        """Generate a JSON response from the LLM."""
        pass


class MockLLM(BaseLLM):
    """Mock LLM for deterministic testing without API keys."""

    # Pre-defined responses for common prompts
    RESPONSES = {
        "prd": """# Product Requirements Document

## Overview
Employee Benefits Information Portal - A web application providing employees with information about company benefits.

## Goals
1. Provide clear information about available benefits
2. Help employees understand eligibility requirements
3. Offer FAQ section for common questions
4. Enable contact with HR for support

## Acceptance Criteria
- Home page with welcome message and navigation
- Benefits overview page listing all benefits
- FAQ page with common questions
- Eligibility checker form
- Contact form for support requests
- Admin page to view submissions""",

        "user_stories": """# User Stories

## Story 1: View Benefits
As an employee, I want to see all available benefits so I can understand what's offered.
Acceptance: Benefits list displays on dedicated page with descriptions.

## Story 2: Check Eligibility
As an employee, I want to check if I'm eligible for benefits so I know what I can enroll in.
Acceptance: Form accepts employment details and shows eligibility results.

## Story 3: Get Answers
As an employee, I want to find answers to common questions so I don't need to contact HR.
Acceptance: FAQ page searchable with relevant questions.

## Story 4: Contact Support
As an employee, I want to submit questions to HR so I can get personalized help.
Acceptance: Contact form submits successfully with confirmation.""",

        "sitemap": """# Sitemap

1. Home (/)
   - Welcome message
   - Quick links to benefits
   
2. Benefits Overview (/benefits)
   - List of all benefits
   - Category filters
   
3. FAQ (/faq)
   - Searchable Q&A
   - Categories
   
4. Eligibility Checker (/eligibility)
   - Input form
   - Results display
   
5. Contact (/contact)
   - Support form
   - Contact information
   
6. Admin (/admin)
   - View submissions
   - Content management""",

        "design_spec": """# Design Specification

## Visual Style
- Professional, clean design
- Corporate blue color scheme (#2563eb primary)
- Readable fonts (system-ui, sans-serif)
- Consistent spacing (8px grid)

## Responsive Behavior
- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px
- Hamburger menu on mobile

## Accessibility
- WCAG 2.1 AA compliance
- Proper heading hierarchy
- Form labels for all inputs
- Alt text for images
- Keyboard navigation support

## Components
- Header with logo and navigation
- Hero section on home page
- Card layout for benefits
- Accordion for FAQs
- Form components with validation states
- Footer with links""",

        "api_spec": """# API Specification

## Endpoints

### GET /api/benefits
Returns list of all benefits.
Response: [{id, name, description, category, eligibility}]

### GET /api/faqs
Returns list of FAQs.
Response: [{id, question, answer, category}]

### POST /api/eligibility
Check eligibility for benefits.
Request: {employment_type, hours_per_week, tenure_months}
Response: {eligible: bool, benefits: [], reason: string}

### POST /api/contact
Submit contact message.
Request: {name, email, subject, message}
Response: {success: bool, message_id: string}

### GET /api/admin/messages
View submitted messages (admin only).
Response: [{id, name, email, subject, message, created_at}]""",

        "database_schema": """-- Database Schema for Employee Benefits Portal

CREATE TABLE IF NOT EXISTS benefits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    eligibility_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS eligibility_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employment_type TEXT NOT NULL,
    hours_per_week INTEGER NOT NULL,
    tenure_months INTEGER NOT NULL,
    is_eligible BOOLEAN NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""",

        "test_plan": """# Test Plan

## Unit Tests
- Test database models
- Test API endpoints
- Test form validation

## Integration Tests
- Test full form submission flow
- Test page rendering with data

## Negative Tests
- Invalid email format
- Missing required fields
- SQL injection attempts
- XSS payload in inputs

## Performance Tests
- Page load under 2 seconds
- API response under 500ms""",

        "assumptions": """# Assumptions

1. Synthetic data only - no real employee information
2. No authentication required for demo purposes
3. Single language (English)
4. No integration with actual HR systems
5. Admin page has no access control in demo
6. Email notifications not implemented
7. No file upload functionality
8. Browser compatibility: Chrome, Firefox, Safari latest""",

        "architecture": """# Architecture

## Tech Stack
- Backend: FastAPI (Python 3.11+)
- Frontend: Jinja2 templates + CSS
- Database: SQLite
- ORM: SQLAlchemy

## Structure
- MVC pattern with separation of concerns
- Routes handle HTTP requests
- Models define data structure
- Templates render HTML
- Static files for CSS/JS

## Data Flow
1. User request hits FastAPI route
2. Route validates input with Pydantic
3. Business logic processes request
4. Database operations via SQLAlchemy
5. Template renders response
6. HTML returned to user""",

        "demo_script": """# Demo Script

## Introduction (30 seconds)
"Today I'll demonstrate AgentSite, a multi-agent framework that builds websites from natural language requirements."

## Run Framework (1 minute)
"Starting with a simple requirement: 'Build an employee benefits portal'"
Run: python cli.py run "Build an employee benefits portal"

## Show Artifacts (1 minute)
"The framework generates 11 artifacts including PRD, design spec, API spec, and security report."
Show: artifacts/ folder contents

## Demo Application (2 minutes)
"Here's the generated Employee Benefits Portal:"
- Home page with navigation
- Benefits overview
- FAQ section
- Eligibility checker form
- Contact form submission
- Admin view of messages

## Quality Gates (1 minute)
"Notice the security audit found no critical issues and all tests passed."
Show: reports/security_report.md

## Conclusion (30 seconds)
"AgentSite demonstrates how multiple AI agents can collaborate to produce production-ready code with built-in quality checks."

## Total Time: 5-6 minutes""",
    }

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate a mock response based on prompt content."""
        prompt_lower = prompt.lower()

        # Match prompt type to predefined response
        if any(word in prompt_lower for word in ["requirements", "prd", "product"]):
            return self.RESPONSES["prd"]
        elif any(word in prompt_lower for word in ["user stories", "stories"]):
            return self.RESPONSES["user_stories"]
        elif any(word in prompt_lower for word in ["sitemap", "site map"]):
            return self.RESPONSES["sitemap"]
        elif any(word in prompt_lower for word in ["design", "visual"]):
            return self.RESPONSES["design_spec"]
        elif any(word in prompt_lower for word in ["api", "endpoint"]):
            return self.RESPONSES["api_spec"]
        elif any(word in prompt_lower for word in ["database", "schema", "sql"]):
            return self.RESPONSES["database_schema"]
        elif any(word in prompt_lower for word in ["test", "qa"]):
            return self.RESPONSES["test_plan"]
        elif any(word in prompt_lower for word in ["assumption"]):
            return self.RESPONSES["assumptions"]
        elif any(word in prompt_lower for word in ["architecture"]):
            return self.RESPONSES["architecture"]
        elif any(word in prompt_lower for word in ["demo", "script"]):
            return self.RESPONSES["demo_script"]
        else:
            # Default generic response
            return f"[MockLLM Response]\n\nGenerated content for: {prompt[:100]}...\n\nThis is a mock response for testing purposes."

    def generate_json(self, prompt: str, system_prompt: str = "") -> dict[str, Any]:
        """Generate a mock JSON response."""
        # Try to extract expected schema from prompt or return generic structure
        if "task" in prompt.lower():
            return {
                "task_id": "task_001",
                "phase": "implementation",
                "assigned_agent": "BackendAgent",
                "goal": "Implement API endpoints",
                "inputs": {"api_spec": "provided"},
                "constraints": ["Use FastAPI", "Validate inputs"],
                "definition_of_done": "All endpoints working with tests",
                "status": "COMPLETED",
                "attempts": 1,
                "result_summary": "Successfully implemented all endpoints",
                "errors": [],
            }
        elif "security" in prompt.lower():
            return {
                "findings": [],
                "risk_level": "LOW",
                "passed": True,
                "summary": "No critical security issues found.",
            }
        else:
            return {"content": self.generate(prompt, system_prompt), "success": True}


class RealLLM(BaseLLM):
    """Real LLM client using OpenAI-compatible API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.openai_api_key
        self.base_url = base_url or settings.openai_base_url
        self.model = model or settings.llm_model

        # Lazy import httpx to avoid dependency if not used
        try:
            import httpx
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=60.0,
            )
        except ImportError:
            raise ImportError("httpx is required for RealLLM. Install with: pip install httpx")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate a response from the real LLM."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self._client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[RealLLM Error] Failed to generate response: {str(e)}"

    def generate_json(self, prompt: str, system_prompt: str = "") -> dict[str, Any]:
        """Generate a JSON response from the real LLM."""
        json_system_prompt = (
            system_prompt + "\n\nRespond ONLY with valid JSON. No markdown, no explanations."
            if system_prompt
            else "Respond ONLY with valid JSON. No markdown, no explanations."
        )

        try:
            content = self.generate(prompt, json_system_prompt)
            # Try to parse as JSON
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            return json.loads(content)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON response: {str(e)}", "raw_content": content}


def get_llm_client() -> BaseLLM:
    """Get appropriate LLM client based on settings."""
    if settings.use_real_llm:
        return RealLLM()
    else:
        return MockLLM()
