# Demo Script: AgentSite Framework

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
