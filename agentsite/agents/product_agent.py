"""Product Agent - Creates PRD, user stories, and assumptions."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class ProductAgent(BaseAgent):
    """Converts user requirements into PRD, user stories, assumptions, and acceptance criteria."""

    name = "ProductAgent"
    role = "Product Manager"
    system_prompt = """You are an expert Product Manager AI agent.
Your task is to analyze user requirements and produce:
1. A comprehensive Product Requirements Document (PRD)
2. Detailed user stories with acceptance criteria
3. Clear assumptions about the project scope
4. Measurable success criteria

Focus on clarity, completeness, and feasibility.
Always use synthetic data - never real personal or company information."""

    input_artifacts = []
    output_artifacts = ["01_prd.md", "02_user_stories.md", "09_assumptions.md"]
    allowed_tools = ["file_read", "file_write"]
    validation_rules = [
        "PRD must include goals and acceptance criteria",
        "User stories must follow 'As a... I want... So that...' format",
        "Assumptions must be clearly documented",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute product analysis task."""
        requirement = task_input.get("requirement", "")

        # Generate PRD
        prd_prompt = f"""Analyze this requirement and create a Product Requirements Document:

Requirement: {requirement}

Create a PRD with:
- Overview
- Goals (3-5 specific goals)
- Target users
- Acceptance criteria
- Out of scope items
- Success metrics"""

        prd_content = self.generate_response(prd_prompt)
        prd_path = self.artifact_store.save("01_prd.md", prd_content)

        # Generate User Stories
        stories_prompt = f"""Based on this requirement, create detailed user stories:

Requirement: {requirement}

Create user stories with:
- Story title
- "As a [user], I want [feature], so that [benefit]"
- Acceptance criteria for each story
- Priority (High/Medium/Low)

Include at least 4-6 user stories."""

        stories_content = self.generate_response(stories_prompt)
        stories_path = self.artifact_store.save("02_user_stories.md", stories_content)

        # Generate Assumptions
        assumptions_prompt = f"""Based on this requirement, document project assumptions:

Requirement: {requirement}

Include assumptions about:
- Data (synthetic only)
- Authentication/authorization
- Integrations
- Browser support
- Performance expectations
- Security considerations
- Known limitations"""

        assumptions_content = self.generate_response(assumptions_prompt)
        assumptions_path = self.artifact_store.save("09_assumptions.md", assumptions_content)

        return {
            "success": True,
            "artifacts": [prd_path, stories_path, assumptions_path],
            "summary": "Generated PRD, user stories, and assumptions",
        }
