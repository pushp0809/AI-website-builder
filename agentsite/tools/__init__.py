"""Tool abstractions for agent operations."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


class FileTools:
    """Safe file read/write operations."""

    @staticmethod
    def read_file(filepath: str, max_size: int = 1024 * 1024) -> str | None:
        """Read file content with size limit."""
        try:
            path = Path(filepath)
            if not path.exists():
                return None
            if path.stat().st_size > max_size:
                raise ValueError(f"File too large: {path.stat().st_size} bytes")
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return None

    @staticmethod
    def write_file(filepath: str, content: str) -> bool:
        """Write content to file safely."""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Check if file exists."""
        return Path(filepath).exists()

    @staticmethod
    def list_directory(dirpath: str) -> list[str]:
        """List directory contents."""
        try:
            return [f.name for f in Path(dirpath).iterdir()]
        except Exception:
            return []


class TerminalTools:
    """Terminal execution with timeout."""

    @staticmethod
    def execute(
        command: str,
        cwd: str | None = None,
        timeout: int = 30,
        capture_output: bool = True,
    ) -> dict[str, Any]:
        """Execute command with timeout."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
            )
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
            }


class LintTools:
    """Code linting operations."""

    @staticmethod
    def run_black(filepath: str, check: bool = True) -> dict[str, Any]:
        """Run black formatter."""
        cmd = f"black {'--check' if check else ''} {filepath}"
        return TerminalTools.execute(cmd, timeout=30)

    @staticmethod
    def run_flake8(filepath: str) -> dict[str, Any]:
        """Run flake8 linter."""
        cmd = f"flake8 {filepath} --max-line-length=120 --ignore=E501,W503"
        return TerminalTools.execute(cmd, timeout=30)

    @staticmethod
    def lint_python_file(filepath: str) -> dict[str, Any]:
        """Run all Python linters on a file."""
        results = {
            "black": LintTools.run_black(filepath),
            "flake8": LintTools.run_flake8(filepath),
        }
        return {
            "passed": all(r["success"] for r in results.values()),
            "details": results,
        }


class TestTools:
    """Testing operations."""

    @staticmethod
    def run_pytest(test_path: str, cwd: str | None = None) -> dict[str, Any]:
        """Run pytest on specified path."""
        cmd = f"pytest {test_path} -v --tb=short"
        result = TerminalTools.execute(cmd, cwd=cwd, timeout=120)
        return {
            "success": result["success"],
            "output": result["stdout"] + result["stderr"],
        }

    @staticmethod
    def run_api_tests(base_url: str, test_file: str) -> dict[str, Any]:
        """Run API tests against a running server."""
        # This would typically use httpx TestClient or similar
        return TestTools.run_pytest(test_file)


class SecurityTools:
    """Security scanning operations."""

    @staticmethod
    def run_bandit(filepath: str) -> dict[str, Any]:
        """Run bandit security scanner."""
        cmd = f"bandit {filepath} -f json -q"
        result = TerminalTools.execute(cmd, timeout=60)
        try:
            import json
            if result["success"]:
                issues = json.loads(result["stdout"]) if result["stdout"] else {"issues": []}
            else:
                issues = {"issues": [], "error": result["stderr"]}
            return {
                "success": True,
                "issues": issues.get("issues", []),
                "severity_counts": issues.get("stats", {}),
            }
        except Exception:
            return {
                "success": False,
                "issues": [],
                "error": result["stderr"],
            }

    @staticmethod
    def scan_for_secrets(content: str) -> list[dict[str, Any]]:
        """Scan content for potential secrets."""
        import re
        findings = []

        # Common secret patterns
        patterns = {
            "api_key": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]",
            "password": r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]+['\"]",
            "secret": r"(?i)(secret|token)\s*[=:]\s*['\"][^'\"]+['\"]",
            "aws_key": r"(?i)AKIA[0-9A-Z]{16}",
            "private_key": r"-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----",
        }

        for secret_type, pattern in patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                findings.append({
                    "type": secret_type,
                    "severity": "HIGH",
                    "description": f"Potential {secret_type} found",
                    "line_sample": matches[0][:50] + "..." if len(matches[0]) > 50 else matches[0],
                })

        return findings

    @staticmethod
    def scan_sql_injection(content: str) -> list[dict[str, Any]]:
        """Scan for potential SQL injection vulnerabilities."""
        findings = []

        # Look for string concatenation with SQL keywords
        dangerous_patterns = [
            r"f\"SELECT.*\{",
            r"f\"INSERT.*\{",
            r"f\"UPDATE.*\{",
            r"f\"DELETE.*\{",
            r"\+.*SELECT.*\+",
            r"'SELECT.*\+",
        ]

        for pattern in dangerous_patterns:
            import re
            if re.search(pattern, content, re.IGNORECASE):
                findings.append({
                    "type": "sql_injection_risk",
                    "severity": "HIGH",
                    "description": "Potential SQL injection vulnerability - use parameterized queries",
                })

        return findings


class GitTools:
    """Git operations."""

    @staticmethod
    def is_git_repo(dirpath: str) -> bool:
        """Check if directory is a git repo."""
        result = TerminalTools.execute("git rev-parse --git-dir", cwd=dirpath)
        return result["success"]

    @staticmethod
    def get_status(dirpath: str) -> str:
        """Get git status."""
        result = TerminalTools.execute("git status", cwd=dirpath)
        return result["stdout"]

    @staticmethod
    def add_and_commit(dirpath: str, message: str) -> dict[str, Any]:
        """Add all files and commit."""
        add_result = TerminalTools.execute("git add -A", cwd=dirpath)
        if not add_result["success"]:
            return add_result
        commit_result = TerminalTools.execute(f'git commit -m "{message}"', cwd=dirpath)
        return commit_result


# Agent role permissions for tools
AGENT_TOOL_PERMISSIONS = {
    "ProductAgent": ["file_read", "file_write"],
    "DesignAgent": ["file_read", "file_write"],
    "FrontendAgent": ["file_read", "file_write", "lint"],
    "BackendAgent": ["file_read", "file_write", "lint", "terminal"],
    "DatabaseAgent": ["file_read", "file_write", "terminal"],
    "IntegrationAgent": ["file_read", "file_write", "terminal", "test"],
    "QAValidatorAgent": ["file_read", "file_write", "terminal", "test", "lint"],
    "SecurityAuditorAgent": ["file_read", "security_scan"],
    "DocumentationAgent": ["file_read", "file_write"],
    "CriticAgent": ["file_read"],
}
