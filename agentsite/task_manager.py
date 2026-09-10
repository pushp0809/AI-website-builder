"""Task manager for structured task tickets."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from agentsite.config import settings
from agentsite.state_manager import TaskStatus


class TaskManager:
    """Manages task tickets and execution tracking."""

    def __init__(self, state_dir: str | None = None):
        self.state_dir = Path(state_dir or settings.state_dir)
        self.tasks_dir = self.state_dir / "tasks"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)

    def create_task(
        self,
        task_id: str,
        phase: str,
        assigned_agent: str,
        goal: str,
        inputs: dict[str, Any] | None = None,
        constraints: list[str] | None = None,
        definition_of_done: str | None = None,
    ) -> dict[str, Any]:
        """Create a new task ticket."""
        task = {
            "task_id": task_id,
            "phase": phase,
            "assigned_agent": assigned_agent,
            "goal": goal,
            "inputs": inputs or {},
            "constraints": constraints or [],
            "definition_of_done": definition_of_done or "Task completed successfully",
            "status": TaskStatus.PENDING.value,
            "attempts": 0,
            "result_summary": None,
            "errors": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": None,
            "started_at": None,
            "completed_at": None,
            "output_artifacts": [],
            "review_status": None,
            "review_comments": None,
        }
        self._save_task(task)
        return task

    def _save_task(self, task: dict[str, Any]) -> None:
        """Save task to file."""
        task["updated_at"] = datetime.now().isoformat()
        filepath = self.tasks_dir / f"{task['task_id']}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(task, f, indent=2)

    def load_task(self, task_id: str) -> dict[str, Any] | None:
        """Load task from file."""
        filepath = self.tasks_dir / f"{task_id}.json"
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def update_status(self, task_id: str, status: TaskStatus) -> None:
        """Update task status."""
        task = self.load_task(task_id)
        if task:
            task["status"] = status.value
            if status == TaskStatus.IN_PROGRESS:
                task["started_at"] = datetime.now().isoformat()
            elif status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                task["completed_at"] = datetime.now().isoformat()
            self._save_task(task)

    def add_attempt(self, task_id: str) -> int:
        """Increment attempt counter."""
        task = self.load_task(task_id)
        if task:
            task["attempts"] += 1
            self._save_task(task)
            return task["attempts"]
        return 0

    def set_result(self, task_id: str, result_summary: str, output_artifacts: list[str] | None = None) -> None:
        """Set task result."""
        task = self.load_task(task_id)
        if task:
            task["result_summary"] = result_summary
            task["output_artifacts"] = output_artifacts or []
            self._save_task(task)

    def add_error(self, task_id: str, error: str) -> None:
        """Add error to task."""
        task = self.load_task(task_id)
        if task:
            task["errors"].append({
                "message": error,
                "timestamp": datetime.now().isoformat(),
            })
            self._save_task(task)

    def set_review(self, task_id: str, approved: bool, comments: str | None = None) -> None:
        """Set review status."""
        task = self.load_task(task_id)
        if task:
            task["review_status"] = "APPROVED" if approved else "REJECTED"
            task["review_comments"] = comments
            self._save_task(task)

    def list_tasks(self, phase: str | None = None, status: TaskStatus | None = None) -> list[dict[str, Any]]:
        """List tasks with optional filters."""
        tasks = []
        for filepath in self.tasks_dir.glob("*.json"):
            with open(filepath, "r", encoding="utf-8") as f:
                task = json.load(f)
                if phase and task.get("phase") != phase:
                    continue
                if status and task.get("status") != status.value:
                    continue
                tasks.append(task)
        return sorted(tasks, key=lambda t: t.get("created_at", ""))

    def get_pending_tasks(self) -> list[dict[str, Any]]:
        """Get all pending tasks."""
        return self.list_tasks(status=TaskStatus.PENDING)

    def get_failed_tasks(self) -> list[dict[str, Any]]:
        """Get all failed tasks."""
        return self.list_tasks(status=TaskStatus.FAILED)

    def get_task_summary(self) -> dict[str, Any]:
        """Get summary of all tasks."""
        tasks = self.list_tasks()
        return {
            "total": len(tasks),
            "by_status": {
                status.value: len([t for t in tasks if t.get("status") == status.value])
                for status in TaskStatus
            },
            "by_phase": {},
        }
