"""Base agent class for all specialist agents."""

from abc import ABC, abstractmethod
from typing import Any

from agentsite.llm_client import BaseLLM, get_llm_client
from agentsite.artifact_store import ArtifactStore
from agentsite.tools import (
    FileTools,
    TerminalTools,
    LintTools,
    TestTools,
    SecurityTools,
    AGENT_TOOL_PERMISSIONS,
)


class BaseAgent(ABC):
    """Abstract base class for all specialist agents."""

    name: str = "BaseAgent"
    role: str = "Base Agent"
    system_prompt: str = "You are a helpful AI assistant."
    allowed_tools: list[str] = []
    input_artifacts: list[str] = []
    output_artifacts: list[str] = []
    validation_rules: list[str] = []

    def __init__(self, llm_client: BaseLLM | None = None, artifact_store: ArtifactStore | None = None):
        self.llm = llm_client or get_llm_client()
        self.artifact_store = artifact_store or ArtifactStore()
        self.allowed_tools = self.allowed_tools or AGENT_TOOL_PERMISSIONS.get(self.name, [])

    @abstractmethod
    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's task. Must be implemented by subclasses."""
        pass

    def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a response using the LLM client."""
        sys_prompt = system_prompt or self.system_prompt
        return self.llm.generate(prompt, sys_prompt)

    def generate_json_response(self, prompt: str, system_prompt: str | None = None) -> dict[str, Any]:
        """Generate a JSON response using the LLM client."""
        sys_prompt = system_prompt or self.system_prompt
        return self.llm.generate_json(prompt, sys_prompt)

    def can_use_tool(self, tool_name: str) -> bool:
        """Check if agent is allowed to use a specific tool."""
        return tool_name in self.allowed_tools

    def read_file(self, filepath: str) -> str | None:
        """Read a file if permitted."""
        if not self.can_use_tool("file_read"):
            raise PermissionError(f"{self.name} is not allowed to read files")
        return FileTools.read_file(filepath)

    def write_file(self, filepath: str, content: str) -> bool:
        """Write a file if permitted."""
        if not self.can_use_tool("file_write"):
            raise PermissionError(f"{self.name} is not allowed to write files")
        return FileTools.write_file(filepath, content)

    def execute_command(self, command: str, cwd: str | None = None, timeout: int = 30) -> dict[str, Any]:
        """Execute a terminal command if permitted."""
        if not self.can_use_tool("terminal"):
            raise PermissionError(f"{self.name} is not allowed to execute commands")
        return TerminalTools.execute(command, cwd=cwd, timeout=timeout)

    def lint_file(self, filepath: str) -> dict[str, Any]:
        """Lint a Python file if permitted."""
        if not self.can_use_tool("lint"):
            raise PermissionError(f"{self.name} is not allowed to lint files")
        return LintTools.lint_python_file(filepath)

    def run_tests(self, test_path: str, cwd: str | None = None) -> dict[str, Any]:
        """Run tests if permitted."""
        if not self.can_use_tool("test"):
            raise PermissionError(f"{self.name} is not allowed to run tests")
        return TestTools.run_pytest(test_path, cwd=cwd)

    def security_scan(self, filepath: str) -> dict[str, Any]:
        """Run security scan if permitted."""
        if not self.can_use_tool("security_scan"):
            raise PermissionError(f"{self.name} is not allowed to run security scans")
        return SecurityTools.run_bandit(filepath)

    def scan_for_secrets(self, content: str) -> list[dict[str, Any]]:
        """Scan content for secrets if permitted."""
        if not self.can_use_tool("security_scan"):
            raise PermissionError(f"{self.name} is not allowed to scan for secrets")
        return SecurityTools.scan_for_secrets(content)

    def load_input_artifacts(self) -> dict[str, str]:
        """Load all input artifacts for this agent."""
        artifacts = {}
        for artifact_name in self.input_artifacts:
            content = self.artifact_store.load(artifact_name)
            if content:
                artifacts[artifact_name] = content
        return artifacts

    def validate_output(self, output: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate output against validation rules."""
        errors = []
        for rule in self.validation_rules:
            # Simple validation - check if rule description is satisfied
            if not self._check_rule(rule, output):
                errors.append(f"Validation failed: {rule}")
        return len(errors) == 0, errors

    def _check_rule(self, rule: str, output: dict[str, Any]) -> bool:
        """Check a single validation rule."""
        # Basic implementation - can be overridden by subclasses
        return True
