"""Validation gates for quality control."""

from agentsite.artifact_store import ArtifactStore
from agentsite.state_manager import StateManager


class ValidationGates:
    """Implements quality gates between pipeline phases."""

    def __init__(self, artifact_store: ArtifactStore, state_manager: StateManager):
        self.artifact_store = artifact_store
        self.state_manager = state_manager

    def check_requirements_gate(self) -> bool:
        """Check if requirements phase outputs meet quality standards."""
        required = ["01_prd.md", "02_user_stories.md", "09_assumptions.md"]
        
        for artifact in required:
            if not self.artifact_store.exists(artifact):
                return False
        
        # Check PRD has content
        prd = self.artifact_store.load("01_prd.md")
        if not prd or len(prd) < 100:
            return False
        
        return True

    def check_design_gate(self) -> bool:
        """Check if design phase outputs meet quality standards."""
        required = ["03_sitemap.md", "04_design_spec.md", "10_architecture.md"]
        
        for artifact in required:
            if not self.artifact_store.exists(artifact):
                return False
        
        return True

    def check_api_gate(self) -> bool:
        """Check if API spec meets quality standards."""
        return self.artifact_store.exists("05_api_spec.yaml")

    def check_database_gate(self) -> bool:
        """Check if database schema meets quality standards."""
        return self.artifact_store.exists("06_database_schema.sql")

    def check_code_quality_gate(self) -> bool:
        """Check if generated code meets quality standards."""
        required = ["main.py", "routes.py", "schemas.py", "models.py"]
        
        for artifact in required:
            if not self.artifact_store.exists(artifact):
                return False
        
        return True

    def check_functional_test_gate(self) -> bool:
        """Check if functional tests pass."""
        state = self.state_manager.get_state()
        gate_result = state.get("gates", {}).get("testing", {})
        return gate_result.get("passed", False)

    def check_security_gate(self) -> bool:
        """Check if security audit passes."""
        state = self.state_manager.get_state()
        gate_result = state.get("gates", {}).get("security", {})
        return gate_result.get("passed", False)

    def check_documentation_gate(self) -> bool:
        """Check if documentation is complete."""
        required = ["README_APP.md", "SECURITY_APP.md", "11_demo_script.md"]
        
        for artifact in required:
            if not self.artifact_store.exists(artifact):
                return False
        
        return True

    def check_all_gates(self) -> dict[str, bool]:
        """Run all gate checks and return results."""
        return {
            "requirements": self.check_requirements_gate(),
            "design": self.check_design_gate(),
            "api": self.check_api_gate(),
            "database": self.check_database_gate(),
            "code_quality": self.check_code_quality_gate(),
            "functional_test": self.check_functional_test_gate(),
            "security": self.check_security_gate(),
            "documentation": self.check_documentation_gate(),
        }
