"""Integration Agent - Connects frontend, backend, and database."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class IntegrationAgent(BaseAgent):
    """Connects frontend, backend, and database. Ensures the app starts and pages/API work together."""

    name = "IntegrationAgent"
    role = "Integration Engineer"
    system_prompt = """You are an expert Integration Engineer AI agent.
Ensure all components work together:
- Frontend templates render correctly
- API endpoints respond properly
- Database queries execute successfully
- Static files are served

Create integration scripts and verify the application runs."""

    input_artifacts = ["main.py", "routes.py", "base.html"]
    output_artifacts = []
    allowed_tools = ["file_read", "file_write", "terminal", "test"]
    validation_rules = [
        "Application must start without errors",
        "All pages must be accessible",
        "API endpoints must return valid responses",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute integration task."""
        # Create run script
        run_script = self._create_run_script()
        run_path = self.artifact_store.save("run_app.sh", run_script)

        # Create test script
        test_script = self._create_test_script()
        test_path = self.artifact_store.save("integration_test.py", test_script)

        return {
            "success": True,
            "artifacts": [run_path, test_path],
            "summary": "Created integration scripts",
        }

    def _create_run_script(self) -> str:
        """Create shell script to run the application."""
        return '''#!/bin/bash
# Run the Employee Benefits Portal

cd "$(dirname "$0")/.."

echo "Starting Employee Benefits Portal..."
echo "Database will be initialized at: generated_app/database.db"

python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000 --reload
'''

    def _create_test_script(self) -> str:
        """Create integration test script."""
        return '''"""Integration tests for Employee Benefits Portal."""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated_app.main import app

client = TestClient(app)


def test_home_page():
    """Test home page loads."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Employee Benefits Portal" in response.content


def test_benefits_page():
    """Test benefits page loads."""
    response = client.get("/benefits")
    assert response.status_code == 200


def test_faq_page():
    """Test FAQ page loads."""
    response = client.get("/faq")
    assert response.status_code == 200


def test_eligibility_page():
    """Test eligibility page loads."""
    response = client.get("/eligibility")
    assert response.status_code == 200


def test_contact_page():
    """Test contact page loads."""
    response = client.get("/contact")
    assert response.status_code == 200


def test_admin_page():
    """Test admin page loads."""
    response = client.get("/admin")
    assert response.status_code == 200


def test_api_benefits():
    """Test benefits API endpoint."""
    response = client.get("/api/benefits")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_api_faqs():
    """Test FAQs API endpoint."""
    response = client.get("/api/faqs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_api_eligibility_valid():
    """Test eligibility check with valid data."""
    payload = {
        "employment_type": "full-time",
        "hours_per_week": 40,
        "tenure_months": 6
    }
    response = client.post("/api/eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "eligible" in data
    assert "reason" in data


def test_api_eligibility_invalid():
    """Test eligibility check with invalid data."""
    payload = {
        "employment_type": "contractor",
        "hours_per_week": 10,
        "tenure_months": 1
    }
    response = client.post("/api/eligibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] == False


def test_api_contact_valid():
    """Test contact form submission with valid data."""
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message."
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True


def test_api_contact_invalid_email():
    """Test contact form with invalid email."""
    payload = {
        "name": "Test User",
        "email": "invalid-email",
        "subject": "Test Subject",
        "message": "This is a test message."
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 400


def test_api_contact_missing_field():
    """Test contact form with missing required field."""
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        # Missing subject and message
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == 422  # Validation error


def test_api_admin_messages():
    """Test admin messages endpoint."""
    response = client.get("/api/admin/messages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
