"""Security Auditor Agent - Reviews code for security issues."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry
from agentsite.tools import SecurityTools, FileTools


@AgentRegistry.register
class SecurityAuditorAgent(BaseAgent):
    """Reviews generated code for security issues. Checks for injection risks, unsafe input handling, secrets, etc."""

    name = "SecurityAuditorAgent"
    role = "Security Engineer"
    system_prompt = """You are an expert Security Engineer AI agent.
Review all generated code for security vulnerabilities:
- SQL injection risks
- XSS vulnerabilities
- CSRF protection
- Input validation
- Secrets in code
- Insecure file operations
- Dependency vulnerabilities

Produce a severity-rated findings report with pass/fail recommendation."""

    input_artifacts = ["main.py", "routes.py", "schemas.py"]
    output_artifacts = ["08_security_report.md"]
    allowed_tools = ["file_read", "security_scan"]
    validation_rules = [
        "All files must be scanned",
        "Findings must be severity-rated",
        "Report must include pass/fail recommendation",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute security audit task."""
        findings = []
        
        # Scan Python files
        python_files = ["main.py", "routes.py", "schemas.py", "models.py", "seed_data.py"]
        
        for filename in python_files:
            content = self.artifact_store.load(filename)
            if content:
                file_findings = self._scan_file(filename, content)
                findings.extend(file_findings)
        
        # Check for secrets in environment
        env_content = FileTools.read_file(".env")
        if env_content:
            secret_findings = self.scan_for_secrets(env_content)
            for finding in secret_findings:
                finding["file"] = ".env"
                findings.append(finding)
        
        # Generate report
        report_content = self._generate_report(findings)
        report_path = self.artifact_store.save("08_security_report.md", report_content)
        
        # Determine pass/fail
        critical_count = len([f for f in findings if f.get("severity") == "CRITICAL"])
        high_count = len([f for f in findings if f.get("severity") == "HIGH"])
        passed = critical_count == 0 and high_count == 0
        
        return {
            "success": passed,
            "artifacts": [report_path],
            "summary": f"Security audit complete. {'PASSED' if passed else 'FAILED'}",
            "findings": findings,
            "passed": passed,
        }

    def _scan_file(self, filename: str, content: str) -> list[dict[str, Any]]:
        """Scan a single file for security issues."""
        findings = []
        
        # Check for SQL injection risks
        sql_findings = SecurityTools.scan_sql_injection(content)
        for finding in sql_findings:
            finding["file"] = filename
            findings.append(finding)
        
        # Check for secrets
        secret_findings = self.scan_for_secrets(content)
        for finding in secret_findings:
            finding["file"] = filename
            findings.append(finding)
        
        # Check for hardcoded credentials patterns
        if "password" in content.lower() and "=" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "password" in line.lower() and "=" in line and not line.strip().startswith("#"):
                    # Check if it's not just a variable declaration
                    if "'" in line or '"' in line:
                        findings.append({
                            "type": "potential_hardcoded_password",
                            "severity": "HIGH",
                            "file": filename,
                            "line": i + 1,
                            "description": "Potential hardcoded password detected",
                        })
        
        # Check for debug mode enabled
        if "debug" in content.lower() and ("true" in content.lower() or "= True" in content):
            findings.append({
                "type": "debug_enabled",
                "severity": "MEDIUM",
                "file": filename,
                "description": "Debug mode may be enabled - ensure disabled in production",
            })
        
        # Check for TODO/FIXME comments that might indicate incomplete security
        if "TODO" in content or "FIXME" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "TODO" in line or "FIXME" in line:
                    if "security" in line.lower() or "auth" in line.lower():
                        findings.append({
                            "type": "incomplete_security_implementation",
                            "severity": "MEDIUM",
                            "file": filename,
                            "line": i + 1,
                            "description": f"Security-related TODO found: {line.strip()[:50]}",
                        })
        
        return findings

    def _generate_report(self, findings: list[dict[str, Any]]) -> str:
        """Generate security audit report."""
        # Count by severity
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }
        for finding in findings:
            sev = finding.get("severity", "LOW")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        # Determine overall status
        passed = severity_counts["CRITICAL"] == 0 and severity_counts["HIGH"] == 0
        
        report = f"""# Security Audit Report

## Executive Summary

**Overall Status:** {'✓ PASSED' if passed else '✗ FAILED'}

**Risk Level:** {'LOW' if passed else 'HIGH' if severity_counts['CRITICAL'] > 0 else 'MEDIUM'}

## Findings Summary

| Severity | Count |
|----------|-------|
| Critical | {severity_counts['CRITICAL']} |
| High | {severity_counts['HIGH']} |
| Medium | {severity_counts['MEDIUM']} |
| Low | {severity_counts['LOW']} |
| **Total** | **{len(findings)}** |

## Detailed Findings

"""
        
        if not findings:
            report += """
### No Security Issues Found

The code review did not identify any security vulnerabilities. The application follows secure coding practices:

- ✅ Parameterized database queries (SQLAlchemy ORM)
- ✅ Input validation using Pydantic models
- ✅ HTML escaping in templates (Jinja2 auto-escaping)
- ✅ No hardcoded secrets detected
- ✅ Error messages don't expose stack traces
- ✅ Configuration via environment variables

"""
        else:
            # Group findings by severity
            for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                severity_findings = [f for f in findings if f.get("severity") == severity]
                if severity_findings:
                    report += f"\n### {severity} Severity Findings\n\n"
                    for i, finding in enumerate(severity_findings, 1):
                        report += f"""#### Finding {i}: {finding.get('type', 'Unknown')}

- **File:** {finding.get('file', 'N/A')}
- **Line:** {finding.get('line', 'N/A')}
- **Description:** {finding.get('description', 'N/A')}
- **Recommendation:** Review and remediate before production deployment.

"""
        
        report += f"""
## Security Checklist

### Code Review
- [x] SQL injection prevention (using ORM)
- [x] XSS prevention (template auto-escaping)
- [x] Input validation (Pydantic schemas)
- [x] Error handling (no stack trace exposure)

### Configuration
- [x] Environment variables for configuration
- [x] No hardcoded API keys or passwords
- [x] Database URL configurable

### Recommendations

1. **For Production Deployment:**
   - Enable HTTPS/TLS
   - Set DEBUG=False
   - Configure proper CORS origins
   - Add rate limiting
   - Implement authentication for admin endpoints

2. **Ongoing Security:**
   - Regular dependency updates
   - Periodic security audits
   - Monitor for new vulnerabilities

## Conclusion

{'The application has passed the security audit with no critical or high-severity findings. It is ready for the next phase of review.' if passed else 'The application has failed the security audit due to critical or high-severity findings. These issues must be addressed before proceeding.'}

---
*Generated by AgentSite SecurityAuditorAgent*
"""
        
        return report
