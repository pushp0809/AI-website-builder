"""State manager for pipeline tracking."""

import json
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from agentsite.config import settings


class TaskStatus(str, Enum):
    """Task status values."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    PASSED = "PASSED"
    COMPLETED = "COMPLETED"


class PhaseStatus(str, Enum):
    """Phase status values."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_GATE = "WAITING_FOR_GATE"
    GATE_FAILED = "GATE_FAILED"
    COMPLETED = "COMPLETED"


class StateManager:
    """Manages pipeline state persistence."""

    def __init__(self, state_dir: str | None = None):
        self.state_dir = Path(state_dir or settings.state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / "state.json"
        self.state = self._load_state()

    def _load_state(self) -> dict[str, Any]:
        """Load state from file or create new state."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Create new state
        return {
            "pipeline_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "requirement": "",
            "started_at": datetime.now().isoformat(),
            "current_phase": None,
            "phases": {},
            "tasks": [],
            "gates": {},
            "metrics": {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "blocked_tasks": 0,
            },
            "artifacts_generated": [],
            "reports_generated": [],
            "final_status": "RUNNING",
            "completed_at": None,
            "error_message": None,
        }

    def save(self) -> None:
        """Save current state to file."""
        self.state["updated_at"] = datetime.now().isoformat()
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2, default=str)

    def set_requirement(self, requirement: str) -> None:
        """Set the user requirement."""
        self.state["requirement"] = requirement
        self.save()

    def set_current_phase(self, phase: str) -> None:
        """Set current phase."""
        self.state["current_phase"] = phase
        if phase and phase not in self.state["phases"]:
            self.state["phases"][phase] = {
                "status": PhaseStatus.IN_PROGRESS.value,
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "gate_status": None,
            }
        self.save()

    def complete_phase(self, phase: str, gate_passed: bool = True) -> None:
        """Mark phase as completed."""
        if phase in self.state["phases"]:
            self.state["phases"][phase]["status"] = PhaseStatus.COMPLETED.value
            self.state["phases"][phase]["completed_at"] = datetime.now().isoformat()
            self.state["phases"][phase]["gate_status"] = "PASSED" if gate_passed else "FAILED"
        self.save()

    def fail_phase(self, phase: str, reason: str) -> None:
        """Mark phase as failed."""
        if phase in self.state["phases"]:
            self.state["phases"][phase]["status"] = PhaseStatus.GATE_FAILED.value
            self.state["phases"][phase]["gate_status"] = "FAILED"
            self.state["phases"][phase]["failure_reason"] = reason
        self.save()

    def add_task(self, task: dict[str, Any]) -> None:
        """Add a task to the state."""
        self.state["tasks"].append(task)
        self.state["metrics"]["total_tasks"] += 1
        self.save()

    def update_task(self, task_id: str, updates: dict[str, Any]) -> None:
        """Update a task's state."""
        for task in self.state["tasks"]:
            if task.get("task_id") == task_id:
                task.update(updates)
                # Update metrics
                if updates.get("status") == TaskStatus.COMPLETED.value:
                    self.state["metrics"]["completed_tasks"] += 1
                elif updates.get("status") == TaskStatus.FAILED.value:
                    self.state["metrics"]["failed_tasks"] += 1
                elif updates.get("status") == TaskStatus.BLOCKED.value:
                    self.state["metrics"]["blocked_tasks"] += 1
                break
        self.save()

    def record_gate(self, gate_name: str, passed: bool, details: dict[str, Any] | None = None) -> None:
        """Record a validation gate result."""
        self.state["gates"][gate_name] = {
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }
        self.save()

    def add_artifact(self, artifact_path: str) -> None:
        """Record a generated artifact."""
        if artifact_path not in self.state["artifacts_generated"]:
            self.state["artifacts_generated"].append(artifact_path)
        self.save()

    def add_report(self, report_path: str) -> None:
        """Record a generated report."""
        if report_path not in self.state["reports_generated"]:
            self.state["reports_generated"].append(report_path)
        self.save()

    def complete_pipeline(self, success: bool = True, error_message: str | None = None) -> None:
        """Mark pipeline as complete."""
        self.state["final_status"] = "SUCCESS" if success else "FAILED"
        self.state["completed_at"] = datetime.now().isoformat()
        if error_message:
            self.state["error_message"] = error_message
        self.save()

    def get_state(self) -> dict[str, Any]:
        """Get current state."""
        return self.state

    def get_summary(self) -> str:
        """Get human-readable summary."""
        s = self.state
        summary = [
            f"Pipeline ID: {s['pipeline_id']}",
            f"Requirement: {s['requirement'][:50]}..." if len(s.get('requirement', '')) > 50 else f"Requirement: {s.get('requirement', 'N/A')}",
            f"Status: {s['final_status']}",
            f"Current Phase: {s['current_phase'] or 'None'}",
            "",
            "Metrics:",
            f"  Total Tasks: {s['metrics']['total_tasks']}",
            f"  Completed: {s['metrics']['completed_tasks']}",
            f"  Failed: {s['metrics']['failed_tasks']}",
            f"  Blocked: {s['metrics']['blocked_tasks']}",
            "",
            "Gates:",
        ]
        for gate_name, gate_result in s.get("gates", {}).items():
            status = "✓" if gate_result.get("passed") else "✗"
            summary.append(f"  {status} {gate_name}")

        if s.get("artifacts_generated"):
            summary.append("")
            summary.append("Artifacts:")
            for artifact in s["artifacts_generated"]:
                summary.append(f"  - {artifact}")

        return "\n".join(summary)
