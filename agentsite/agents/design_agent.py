"""Design Agent - Creates sitemap, design spec, and architecture."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class DesignAgent(BaseAgent):
    """Produces sitemap, page structure, component list, accessibility requirements, and responsive behavior."""

    name = "DesignAgent"
    role = "UX/UI Designer"
    system_prompt = """You are an expert UX/UI Designer AI agent.
Your task is to create:
1. A clear sitemap with all pages and navigation
2. Detailed design specifications
3. Component inventory
4. Accessibility requirements (WCAG 2.1 AA)
5. Responsive behavior specifications

Focus on professional, clean design that works across devices.
Ensure all interactive elements are accessible."""

    input_artifacts = ["01_prd.md", "02_user_stories.md"]
    output_artifacts = ["03_sitemap.md", "04_design_spec.md", "10_architecture.md"]
    allowed_tools = ["file_read", "file_write"]
    validation_rules = [
        "Sitemap must include all required pages",
        "Design spec must address accessibility",
        "Architecture must specify tech stack",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute design task."""
        # Load input artifacts
        prd = self.artifact_store.load("01_prd.md") or ""
        user_stories = self.artifact_store.load("02_user_stories.md") or ""

        # Generate Sitemap
        sitemap_prompt = f"""Based on these requirements, create a sitemap:

PRD Summary: {prd[:500]}...
User Stories: {user_stories[:500]}...

Create a sitemap including:
- All pages with their URLs
- Navigation hierarchy
- Key components on each page
- Internal linking strategy

For an Employee Benefits Portal, ensure these pages exist:
- Home (/)
- Benefits Overview (/benefits)
- FAQ (/faq)
- Eligibility Checker (/eligibility)
- Contact (/contact)
- Admin (/admin)"""

        sitemap_content = self.generate_response(sitemap_prompt)
        sitemap_path = self.artifact_store.save("03_sitemap.md", sitemap_content)

        # Generate Design Spec
        design_prompt = f"""Create a detailed design specification:

Requirements: {prd[:500]}...

Include:
- Visual style (colors, typography, spacing)
- Responsive breakpoints
- Accessibility requirements (WCAG 2.1 AA)
- Component specifications
- Form design patterns
- Error state designs
- Loading states

Use a professional corporate blue color scheme."""

        design_content = self.generate_response(design_prompt)
        design_path = self.artifact_store.save("04_design_spec.md", design_content)

        # Generate Architecture
        arch_prompt = f"""Create a technical architecture document:

Project type: Employee Benefits Portal

Include:
- Tech stack (FastAPI backend, Jinja2 templates, SQLite database)
- Project structure
- Data flow diagrams
- API design patterns
- Database ORM approach
- Security considerations

Format as Markdown with Mermaid diagrams where helpful."""

        arch_content = self.generate_response(arch_prompt)
        arch_path = self.artifact_store.save("10_architecture.md", arch_content)

        return {
            "success": True,
            "artifacts": [sitemap_path, design_path, arch_path],
            "summary": "Generated sitemap, design spec, and architecture",
        }
