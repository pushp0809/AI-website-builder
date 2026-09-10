"""Artifact store for structured outputs."""

import os
from pathlib import Path
from typing import Any

from agentsite.config import settings


class ArtifactStore:
    """Manages storage and retrieval of generated artifacts."""

    REQUIRED_ARTIFACTS = [
        "01_prd.md",
        "02_user_stories.md",
        "03_sitemap.md",
        "04_design_spec.md",
        "05_api_spec.yaml",
        "06_database_schema.sql",
        "07_test_plan.md",
        "08_security_report.md",
        "09_assumptions.md",
        "10_architecture.md",
        "11_demo_script.md",
    ]

    def __init__(self, artifacts_dir: str | None = None):
        self.artifacts_dir = Path(artifacts_dir or settings.artifacts_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, content: str) -> str:
        """Save artifact content to file."""
        filepath = self.artifacts_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return str(filepath)

    def load(self, filename: str) -> str | None:
        """Load artifact content from file."""
        filepath = self.artifacts_dir / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def exists(self, filename: str) -> bool:
        """Check if artifact exists."""
        return (self.artifacts_dir / filename).exists()

    def list_artifacts(self) -> list[str]:
        """List all artifacts in the store."""
        return [f.name for f in self.artifacts_dir.iterdir() if f.is_file()]

    def get_path(self, filename: str) -> Path:
        """Get full path to an artifact."""
        return self.artifacts_dir / filename

    def save_json(self, filename: str, data: dict[str, Any]) -> str:
        """Save JSON artifact."""
        import json
        filepath = self.artifacts_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return str(filepath)

    def load_json(self, filename: str) -> dict[str, Any] | None:
        """Load JSON artifact."""
        import json
        filepath = self.artifacts_dir / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def check_required_artifacts(self) -> dict[str, bool]:
        """Check which required artifacts exist."""
        return {artifact: self.exists(artifact) for artifact in self.REQUIRED_ARTIFACTS}

    def get_missing_artifacts(self) -> list[str]:
        """Get list of missing required artifacts."""
        return [a for a, exists in self.check_required_artifacts().items() if not exists]
