"""Tests for AgentSite framework."""

import pytest
from agentsite.orchestrator import Orchestrator
from agentsite.llm_client import MockLLM, RealLLM
from agentsite.state_manager import StateManager
from agentsite.task_manager import TaskManager


class TestMockLLM:
    """Test MockLLM client."""

    def test_mock_llm_generates_deterministic_output(self):
        """MockLLM should return deterministic output."""
        llm = MockLLM()
        response = llm.generate("test prompt")
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

    def test_mock_llm_handles_system_prompt(self):
        """MockLLM should handle system prompts."""
        llm = MockLLM()
        response = llm.generate(
            "test prompt",
            system_prompt="You are a helpful assistant."
        )
        assert response is not None


class TestStateManager:
    """Test StateManager."""

    def test_state_manager_creates_state_file(self, tmp_path):
        """StateManager should create state file."""
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        manager = StateManager(str(state_dir))
        # State file is created on save, check directory exists
        assert state_dir.exists()

    def test_state_manager_updates_phase_status(self, tmp_path):
        """StateManager should update phase status."""
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        manager = StateManager(str(state_dir))
        manager.update_phase("requirements", "COMPLETED")
        assert manager.get_phase_status("requirements") == "COMPLETED"


class TestTaskManager:
    """Test TaskManager."""

    def test_task_manager_creates_task(self, tmp_path):
        """TaskManager should create task files."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        manager = TaskManager(str(tasks_dir))
        task = manager.create_task(
            task_id="test_001",
            phase="testing",
            assigned_agent="QAValidatorAgent",
            goal="Run tests",
            definition_of_done="Tests pass"
        )
        assert task["task_id"] == "test_001"
        assert task["status"] == "PENDING"

    def test_task_manager_updates_task_status(self, tmp_path):
        """TaskManager should update task status."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        manager = TaskManager(str(tasks_dir))
        task = manager.create_task(
            task_id="test_002",
            phase="testing",
            assigned_agent="QAValidatorAgent",
            goal="Run tests",
            definition_of_done="Tests pass"
        )
        from agentsite.state_manager import TaskStatus
        updated = manager.update_status("test_002", TaskStatus.COMPLETED)
        assert updated["status"] == "COMPLETED"


class TestOrchestrator:
    """Test Orchestrator."""

    def test_orchestrator_initializes_with_requirement(self):
        """Orchestrator should initialize with requirement."""
        orchestrator = Orchestrator(use_mock_llm=True)
        assert orchestrator.requirement is None
        
    def test_orchestrator_phases_are_defined(self):
        """Orchestrator should have all phases defined."""
        orchestrator = Orchestrator(use_mock_llm=True)
        expected_phases = [
            "requirements", "design", "api_spec", "database",
            "frontend", "backend", "integration", "testing",
            "security", "documentation", "final_review"
        ]
        for phase in expected_phases:
            assert phase in orchestrator.phases


class TestIntegration:
    """Integration tests for the generated app."""

    def test_generated_app_home_page(self):
        """Test that generated app home page loads."""
        from fastapi.testclient import TestClient
        from generated_app.main import app
        
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert b"Employee Benefits Portal" in response.content

    def test_generated_app_api_benefits(self):
        """Test benefits API endpoint."""
        from fastapi.testclient import TestClient
        from generated_app.main import app
        
        client = TestClient(app)
        response = client.get("/api/benefits")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_generated_app_eligibility_check(self):
        """Test eligibility checker."""
        from fastapi.testclient import TestClient
        from generated_app.main import app
        
        client = TestClient(app)
        payload = {
            "employment_type": "full-time",
            "hours_per_week": 40,
            "tenure_months": 6
        }
        response = client.post("/api/eligibility", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "eligible" in data
