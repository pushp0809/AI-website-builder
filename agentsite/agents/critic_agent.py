"""Critic Agent - Reviews outputs against definition of done."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class CriticAgent(BaseAgent):
    """Reviews outputs against the definition of done. Can reject tasks and request rework."""

    name = "CriticAgent"
    role = "Quality Assurance Reviewer"
    system_prompt = """You are an expert Quality Assurance Reviewer AI agent.
Your role is to:
- Review all generated artifacts against quality criteria
- Approve or reject task outputs
- Provide clear feedback for rework when needed
- Ensure consistency across all deliverables

Be thorough but fair. Reject only when quality standards are not met."""

    input_artifacts = []
    output_artifacts = []
    allowed_tools = ["file_read"]
    validation_rules = [
        "Must provide clear approval/rejection decision",
        "Must explain reasoning",
        "Must suggest improvements if rejecting",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute review task."""
        artifact_type = task_input.get("artifact_type", "")
        artifact_name = task_input.get("artifact_name", "")
        definition_of_done = task_input.get("definition_of_done", "")

        # Load the artifact to review
        content = self.artifact_store.load(artifact_name)
        if not content:
            return {
                "success": False,
                "approved": False,
                "reason": f"Artifact '{artifact_name}' not found",
                "suggestions": ["Ensure the artifact is generated before review"],
            }

        # Perform review
        review_result = self._review_artifact(artifact_type, content, definition_of_done)

        return {
            "success": True,
            "approved": review_result["approved"],
            "reason": review_result["reason"],
            "suggestions": review_result.get("suggestions", []),
            "quality_score": review_result.get("quality_score", 0),
        }

    def _review_artifact(self, artifact_type: str, content: str, dod: str) -> dict[str, Any]:
        """Review an artifact against its type-specific criteria."""
        
        # Generic review criteria
        issues = []
        suggestions = []
        
        # Check minimum length
        if len(content) < 50:
            issues.append("Content is too short")
            suggestions.append("Expand the content with more detail")
        
        # Check for placeholder text
        placeholders = ["TODO", "FIXME", "placeholder", "TBD", "[insert"]
        for placeholder in placeholders:
            if placeholder.lower() in content.lower():
                issues.append(f"Contains placeholder text: {placeholder}")
                suggestions.append(f"Replace all instances of '{placeholder}' with actual content")
        
        # Type-specific review
        if artifact_type == "prd":
            return self._review_prd(content, issues, suggestions)
        elif artifact_type == "user_stories":
            return self._review_user_stories(content, issues, suggestions)
        elif artifact_type == "design_spec":
            return self._review_design_spec(content, issues, suggestions)
        elif artifact_type == "api_spec":
            return self._review_api_spec(content, issues, suggestions)
        elif artifact_type == "database_schema":
            return self._review_database_schema(content, issues, suggestions)
        elif artifact_type == "code":
            return self._review_code(content, issues, suggestions)
        elif artifact_type == "security_report":
            return self._review_security_report(content, issues, suggestions)
        elif artifact_type == "test_report":
            return self._review_test_report(content, issues, suggestions)
        else:
            return self._generic_review(content, issues, suggestions)

    def _review_prd(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review PRD document."""
        required_sections = ["goal", "overview", "acceptance"]
        for section in required_sections:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")
                suggestions.append(f"Add a {section} section to the PRD")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "PRD meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 10 if approved else 5,
        }

    def _review_user_stories(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review user stories document."""
        if "as a" not in content.lower():
            issues.append("User stories don't follow 'As a...' format")
            suggestions.append("Rewrite stories using standard format: 'As a [user], I want [feature], so that [benefit]'")
        
        if "acceptance" not in content.lower():
            issues.append("Missing acceptance criteria")
            suggestions.append("Add acceptance criteria to each user story")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "User stories meet quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 10 if approved else 5,
        }

    def _review_design_spec(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review design specification."""
        design_elements = ["color", "responsive", "accessibility"]
        for element in design_elements:
            if element.lower() not in content.lower():
                suggestions.append(f"Consider adding more detail about {element}")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Design spec meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 9 if approved else 6,
        }

    def _review_api_spec(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review API specification."""
        if "openapi" not in content.lower() and "swagger" not in content.lower():
            suggestions.append("Consider using OpenAPI/Swagger format for API spec")
        
        if "path" not in content.lower() and "endpoint" not in content.lower():
            issues.append("API spec missing endpoint definitions")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "API spec meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 9 if approved else 6,
        }

    def _review_database_schema(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review database schema."""
        if "create table" not in content.lower():
            issues.append("Database schema missing table definitions")
        
        if "primary key" not in content.lower():
            issues.append("Tables should have primary keys")
            suggestions.append("Add PRIMARY KEY to all tables")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Database schema meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 9 if approved else 5,
        }

    def _review_code(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review code file."""
        # Check for basic code quality issues
        if "import *" in content:
            issues.append("Wildcard imports should be avoided")
            suggestions.append("Use explicit imports instead of 'import *'")
        
        if "eval(" in content or "exec(" in content:
            issues.append("Use of eval/exec is a security risk")
            suggestions.append("Remove eval/exec calls and use safer alternatives")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Code meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 10 if approved else 3,
        }

    def _review_security_report(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review security report."""
        if "passed" not in content.lower() and "failed" not in content.lower():
            issues.append("Security report missing pass/fail conclusion")
        
        if "finding" not in content.lower() and "issue" not in content.lower():
            suggestions.append("Consider adding detailed findings section")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Security report meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 9 if approved else 7,
        }

    def _review_test_report(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Review test report."""
        if "passed" not in content.lower() and "failed" not in content.lower():
            issues.append("Test report missing test results")
        
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Test report meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 9 if approved else 6,
        }

    def _generic_review(self, content: str, issues: list, suggestions: list) -> dict[str, Any]:
        """Generic review for unspecified artifact types."""
        approved = len(issues) == 0
        return {
            "approved": approved,
            "reason": "Artifact meets quality standards" if approved else "; ".join(issues),
            "suggestions": suggestions,
            "quality_score": 8 if approved else 6,
        }
