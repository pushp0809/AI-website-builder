"""Documentation Agent - Writes README, architecture docs, and demo script."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class DocumentationAgent(BaseAgent):
    """Writes README, architecture overview, assumptions, limitations, setup instructions, and demo script."""

    name = "DocumentationAgent"
    role = "Technical Writer"
    system_prompt = """You are an expert Technical Writer AI agent.
Create comprehensive documentation including:
- README with setup instructions
- Architecture overview
- Assumptions and limitations
- Demo script for presentations
- Security documentation

Write clear, professional documentation suitable for both developers and stakeholders."""

    input_artifacts = ["01_prd.md", "10_architecture.md", "09_assumptions.md"]
    output_artifacts = []
    allowed_tools = ["file_read", "file_write"]
    validation_rules = [
        "README must include installation steps",
        "Architecture must have diagram",
        "Demo script must be executable",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute documentation generation task."""
        artifacts = []

        # Generate README
        readme_content = self._generate_readme()
        artifacts.append(self.artifact_store.save("README_APP.md", readme_content))

        # Generate security docs
        security_content = self._generate_security_docs()
        artifacts.append(self.artifact_store.save("SECURITY_APP.md", security_content))

        # Generate demo script
        demo_content = self._generate_demo_script()
        artifacts.append(self.artifact_store.save("11_demo_script.md", demo_content))

        return {
            "success": True,
            "artifacts": artifacts,
            "summary": f"Generated {len(artifacts)} documentation files",
        }

    def _generate_readme(self) -> str:
        """Generate README for the generated application."""
        return '''# Employee Benefits Portal

A web application providing employees with information about company benefits.

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 sqlalchemy pydantic python-dotenv

# Run the application
python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000
```

## Features

- **Benefits Overview**: Browse all available employee benefits
- **FAQ Section**: Find answers to common questions
- **Eligibility Checker**: Determine which benefits you qualify for
- **Contact Form**: Submit questions to HR support
- **Admin Dashboard**: View submitted messages

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Welcome page with quick links |
| Benefits | `/benefits` | List of all available benefits |
| FAQ | `/faq` | Frequently asked questions |
| Eligibility | `/eligibility` | Check your benefit eligibility |
| Contact | `/contact` | Submit a support request |
| Admin | `/admin` | View submitted messages |

## API Endpoints

- `GET /api/benefits` - Get all benefits
- `GET /api/faqs` - Get all FAQs
- `POST /api/eligibility` - Check eligibility
- `POST /api/contact` - Submit contact message
- `GET /api/admin/messages` - View messages (admin)

## Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Jinja2 templates + CSS
- **Database**: SQLite
- **ORM**: SQLAlchemy

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=sqlite:///generated_app/database.db
SECRET_KEY=your-secret-key-here
DEBUG=false
```

## Development

```bash
# Run with auto-reload
python -m uvicorn generated_app.main:app --reload

# Run tests
pytest generated_app/integration_test.py -v
```

## Important Notes

- This is a **demo application** using **synthetic data only**
- No real personal or company information is included
- Admin endpoints have no authentication in this demo
- Not intended for production use without additional security measures

## License

MIT License
'''

    def _generate_security_docs(self) -> str:
        """Generate security documentation."""
        return '''# Security Documentation

## Security Measures Implemented

### Input Validation
- All form inputs validated using Pydantic schemas
- Email format validation
- Length limits on all text fields
- Type coercion and validation

### SQL Injection Prevention
- SQLAlchemy ORM used for all database operations
- Parameterized queries throughout
- No raw SQL string concatenation

### XSS Prevention
- Jinja2 template auto-escaping enabled
- HTML entity encoding for user-submitted content
- No inline JavaScript execution from user data

### Error Handling
- Generic error messages shown to users
- Stack traces not exposed in responses
- Custom exception handler for unexpected errors

### Configuration Security
- Secrets loaded from environment variables
- Default secret key must be changed for production
- Database URL configurable

## Security Recommendations for Production

1. **Authentication & Authorization**
   - Implement user authentication
   - Add role-based access control
   - Protect admin endpoints

2. **HTTPS/TLS**
   - Enable HTTPS in production
   - Use valid SSL certificates
   - Redirect HTTP to HTTPS

3. **Rate Limiting**
   - Add rate limiting to prevent abuse
   - Configure per-endpoint limits

4. **CORS Configuration**
   - Set specific allowed origins
   - Don't use wildcard (*) in production

5. **Session Management**
   - Implement secure session handling
   - Use HTTP-only cookies
   - Set appropriate session timeouts

6. **Logging & Monitoring**
   - Log security events
   - Monitor for suspicious activity
   - Set up alerting

## Known Limitations (Demo Version)

- No user authentication
- Admin endpoints publicly accessible
- No CSRF protection implemented
- No rate limiting
- SQLite database (not suitable for high traffic)

## Compliance Considerations

This demo application is not compliant with:
- HIPAA (healthcare data)
- GDPR (EU privacy regulations)
- SOC 2 (security controls)

For production use, additional measures must be implemented.

## Reporting Security Issues

If you discover security vulnerabilities, please report them responsibly.

---
*Generated by AgentSite SecurityAuditorAgent*
'''

    def _generate_demo_script(self) -> str:
        """Generate demo script for presentations."""
        return '''# Demo Script: AgentSite Framework

## Duration: 5-7 minutes

---

## Introduction (30 seconds)

"Good [morning/afternoon], today I'll demonstrate AgentSite, a multi-agent framework that automatically builds websites from natural language requirements."

**Show:** Title slide or terminal window

---

## Step 1: Show the Requirement (30 seconds)

"Let's start with a simple business requirement: Build an employee benefits portal."

**Show:** 
```bash
python cli.py run "Build an employee benefits portal"
```

**Say:** "With one command, AgentSite orchestrates 10 specialized AI agents to design, build, test, and document a complete web application."

---

## Step 2: Show Generated Artifacts (1 minute)

"While the application builds, let me show you the artifacts being generated."

**Show:** `ls -la artifacts/`

**Say:** 
- "01_prd.md - Product Requirements Document"
- "03_sitemap.md - Site structure and navigation"
- "04_design_spec.md - Visual design specifications"
- "05_api_spec.yaml - OpenAPI specification"
- "06_database_schema.sql - Database design"
- "08_security_report.md - Security audit findings"

**Key point:** "Every artifact is tracked and versioned. The CriticAgent reviews each output against quality gates before proceeding."

---

## Step 3: Run the Application (1 minute)

"Now let's see the generated application in action."

**Show:**
```bash
python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000
```

**Navigate to:** http://localhost:8000

**Say:** "This is a fully functional Employee Benefits Portal built entirely by AI agents."

---

## Step 4: Demo the Application (2 minutes)

### Home Page (30 seconds)
**Show:** Navigation, hero section, feature cards
**Say:** "Clean, responsive design with professional styling."

### Benefits Page (30 seconds)
**Click:** Benefits link
**Say:** "Benefits are loaded dynamically from the database via the API."

### Eligibility Checker (45 seconds)
**Click:** Eligibility link
**Fill form:** Full-time, 40 hours, 6 months
**Submit:** Show eligibility result
**Say:** "The form validates input and provides immediate feedback. Let's try a negative case..."
**Fill form:** Contractor, 10 hours, 1 month
**Submit:** Show not eligible message

### Contact Form (15 seconds)
**Click:** Contact link
**Say:** "Form submissions are saved to the database and visible in the admin dashboard."

---

## Step 5: Show Quality Reports (1 minute)

**Show:** `cat reports/security_report.md`

**Say:** 
"The SecurityAuditorAgent scanned all generated code and found no critical issues."

**Show:** `cat artifacts/test_report.md`

"All integration tests passed, verifying API endpoints and form validation."

---

## Step 6: Architecture Overview (30 seconds)

**Show:** ARCHITECTURE.md with Mermaid diagram

**Say:** 
"AgentSite uses a modular architecture with specialized agents, a central orchestrator, and strict quality gates. This ensures consistent, high-quality output."

---

## Conclusion (30 seconds)

"In just a few minutes, AgentSite has:"
- "Analyzed requirements"
- "Designed the application"
- "Generated frontend and backend code"
- "Created a database with synthetic data"
- "Run security audits"
- "Executed integration tests"
- "Produced comprehensive documentation"

"This demonstrates the power of multi-agent AI systems for software development. Thank you!"

---

## Q&A Preparation

**Common Questions:**

1. **"Can it handle complex requirements?"**
   - "The framework scales by adding more specialized agents. Complex projects may require human review at quality gates."

2. **"Is the code production-ready?"**
   - "The generated code follows best practices but should be reviewed before production deployment, especially for security and compliance."

3. **"What about authentication?"**
   - "The demo doesn't include auth, but the architecture supports adding an AuthAgent for that functionality."

4. **"How does it compare to low-code platforms?"**
   - "Unlike low-code, AgentSite generates standard code that developers can understand, modify, and extend."

---

## Backup Demos

If something fails:
1. Show pre-generated screenshots
2. Display sample artifacts
3. Walk through the architecture diagram
'''
