"""Frontend Agent - Creates HTML templates and CSS."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class FrontendAgent(BaseAgent):
    """Generates frontend pages/components based on approved design spec."""

    name = "FrontendAgent"
    role = "Frontend Developer"
    system_prompt = """You are an expert Frontend Developer AI agent.
Create clean, accessible HTML templates with:
- Semantic HTML5
- Proper form labels
- Responsive CSS
- Professional styling
- No inline JavaScript

Use a corporate blue color scheme (#2563eb primary)."""

    input_artifacts = ["03_sitemap.md", "04_design_spec.md"]
    output_artifacts = []
    allowed_tools = ["file_read", "file_write"]
    validation_rules = [
        "All forms must have labels",
        "Responsive design required",
        "Accessible navigation",
        "No hardcoded secrets",
    ]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute frontend generation task."""
        import os
        from pathlib import Path
        
        # Create generated_app directories
        generated_app_dir = Path("generated_app")
        templates_dir = generated_app_dir / "templates"
        static_dir = generated_app_dir / "static"
        
        generated_app_dir.mkdir(exist_ok=True)
        templates_dir.mkdir(exist_ok=True)
        static_dir.mkdir(exist_ok=True)
        
        artifacts = []

        # Generate base template
        base_content = self._generate_base_template()
        base_path = templates_dir / "base.html"
        with open(base_path, "w") as f:
            f.write(base_content)
        artifacts.append(str(base_path))

        # Generate page templates
        home_content = self._generate_home_page()
        home_path = templates_dir / "home.html"
        with open(home_path, "w") as f:
            f.write(home_content)
        artifacts.append(str(home_path))

        benefits_content = self._generate_benefits_page()
        benefits_path = templates_dir / "benefits.html"
        with open(benefits_path, "w") as f:
            f.write(benefits_content)
        artifacts.append(str(benefits_path))

        faq_content = self._generate_faq_page()
        faq_path = templates_dir / "faq.html"
        with open(faq_path, "w") as f:
            f.write(faq_content)
        artifacts.append(str(faq_path))

        eligibility_content = self._generate_eligibility_page()
        eligibility_path = templates_dir / "eligibility.html"
        with open(eligibility_path, "w") as f:
            f.write(eligibility_content)
        artifacts.append(str(eligibility_path))

        contact_content = self._generate_contact_page()
        contact_path = templates_dir / "contact.html"
        with open(contact_path, "w") as f:
            f.write(contact_content)
        artifacts.append(str(contact_path))

        admin_content = self._generate_admin_page()
        admin_path = templates_dir / "admin.html"
        with open(admin_path, "w") as f:
            f.write(admin_content)
        artifacts.append(str(admin_path))

        # Generate CSS
        css_content = self._generate_css()
        css_path = static_dir / "style.css"
        with open(css_path, "w") as f:
            f.write(css_content)
        artifacts.append(str(css_path))

        return {
            "success": True,
            "artifacts": artifacts,
            "summary": f"Generated {len(artifacts)} frontend files",
        }

    def _generate_base_template(self) -> str:
        """Generate base HTML template."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Employee Benefits Portal{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="/" class="logo">BenefitsPortal</a>
            <button class="nav-toggle" aria-label="Toggle navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/benefits">Benefits</a></li>
                <li><a href="/faq">FAQ</a></li>
                <li><a href="/eligibility">Eligibility</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/admin" class="admin-link">Admin</a></li>
            </ul>
        </nav>
    </header>

    <main class="main">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Employee Benefits Portal. All rights reserved.</p>
            <p class="disclaimer">This is a demo application using synthetic data only.</p>
        </div>
    </footer>

    <script>
        // Mobile nav toggle
        document.querySelector('.nav-toggle')?.addEventListener('click', function() {
            document.querySelector('.nav-menu').classList.toggle('active');
        });
    </script>
</body>
</html>
'''

    def _generate_home_page(self) -> str:
        """Generate home page template."""
        return '''{% extends "base.html" %}

{% block title %}Home - Employee Benefits Portal{% endblock %}

{% block content %}
<section class="hero">
    <h1>Welcome to the Employee Benefits Portal</h1>
    <p class="hero-subtitle">Your comprehensive resource for understanding and managing your employee benefits.</p>
    <div class="hero-actions">
        <a href="/benefits" class="btn btn-primary">View Benefits</a>
        <a href="/eligibility" class="btn btn-secondary">Check Eligibility</a>
    </div>
</section>

<section class="features">
    <h2>What You Can Do Here</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <h3>📋 Browse Benefits</h3>
            <p>Explore all available benefits including health insurance, retirement plans, and more.</p>
            <a href="/benefits">Learn more →</a>
        </div>
        <div class="feature-card">
            <h3>❓ Get Answers</h3>
            <p>Find answers to frequently asked questions about your benefits.</p>
            <a href="/faq">View FAQs →</a>
        </div>
        <div class="feature-card">
            <h3>✓ Check Eligibility</h3>
            <p>Determine which benefits you're eligible for based on your employment status.</p>
            <a href="/eligibility">Check now →</a>
        </div>
        <div class="feature-card">
            <h3>📧 Contact Support</h3>
            <p>Have questions? Reach out to our HR support team for assistance.</p>
            <a href="/contact">Get in touch →</a>
        </div>
    </div>
</section>
{% endblock %}
'''

    def _generate_benefits_page(self) -> str:
        """Generate benefits page template."""
        return '''{% extends "base.html" %}

{% block title %}Benefits Overview - Employee Benefits Portal{% endblock %}

{% block content %}
<h1>Benefits Overview</h1>
<p class="page-intro">We offer a comprehensive benefits package designed to support you and your family.</p>

<div id="benefits-list" class="benefits-grid">
    <!-- Benefits will be loaded dynamically -->
    <div class="loading">Loading benefits...</div>
</div>

<script>
async function loadBenefits() {
    try {
        const response = await fetch('/api/benefits');
        const benefits = await response.json();
        
        const container = document.getElementById('benefits-list');
        if (benefits.length === 0) {
            container.innerHTML = '<p>No benefits available at this time.</p>';
            return;
        }
        
        container.innerHTML = benefits.map(benefit => `
            <div class="benefit-card">
                <span class="benefit-category">${benefit.category}</span>
                <h3>${benefit.name}</h3>
                <p>${benefit.description}</p>
                ${benefit.eligibility_requirements ? `
                    <p class="eligibility-req"><strong>Eligibility:</strong> ${benefit.eligibility_requirements}</p>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('benefits-list').innerHTML = 
            '<p class="error">Failed to load benefits. Please try again later.</p>';
    }
}
loadBenefits();
</script>
{% endblock %}
'''

    def _generate_faq_page(self) -> str:
        """Generate FAQ page template."""
        return '''{% extends "base.html" %}

{% block title %}FAQ - Employee Benefits Portal{% endblock %}

{% block content %}
<h1>Frequently Asked Questions</h1>
<p class="page-intro">Find answers to common questions about your benefits.</p>

<div class="search-box">
    <input type="text" id="faq-search" placeholder="Search FAQs..." aria-label="Search FAQs">
</div>

<div id="faqs-list" class="faqs-list">
    <!-- FAQs will be loaded dynamically -->
    <div class="loading">Loading FAQs...</div>
</div>

<script>
async function loadFAQs() {
    try {
        const response = await fetch('/api/faqs');
        const faqs = await response.json();
        
        const container = document.getElementById('faqs-list');
        if (faqs.length === 0) {
            container.innerHTML = '<p>No FAQs available at this time.</p>';
            return;
        }
        
        container.innerHTML = faqs.map((faq, index) => `
            <details class="faq-item">
                <summary>${faq.question}</summary>
                <p>${faq.answer}</p>
            </details>
        `).join('');
    } catch (error) {
        document.getElementById('faqs-list').innerHTML = 
            '<p class="error">Failed to load FAQs. Please try again later.</p>';
    }
}

// Search functionality
document.getElementById('faq-search')?.addEventListener('input', function(e) {
    const search = e.target.value.toLowerCase();
    document.querySelectorAll('.faq-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(search) ? '' : 'none';
    });
});

loadFAQs();
</script>
{% endblock %}
'''

    def _generate_eligibility_page(self) -> str:
        """Generate eligibility checker page template."""
        return '''{% extends "base.html" %}

{% block title %}Eligibility Checker - Employee Benefits Portal{% endblock %}

{% block content %}
<h1>Benefits Eligibility Checker</h1>
<p class="page-intro">Find out which benefits you're eligible for based on your employment details.</p>

<form id="eligibility-form" class="form" onsubmit="return checkEligibility(event)">
    <div class="form-group">
        <label for="employment_type">Employment Type</label>
        <select id="employment_type" name="employment_type" required>
            <option value="">Select employment type</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contractor">Contractor</option>
        </select>
    </div>
    
    <div class="form-group">
        <label for="hours_per_week">Hours Per Week</label>
        <input type="number" id="hours_per_week" name="hours_per_week" 
               min="0" max="100" required placeholder="e.g., 40">
    </div>
    
    <div class="form-group">
        <label for="tenure_months">Months of Employment</label>
        <input type="number" id="tenure_months" name="tenure_months" 
               min="0" max="600" required placeholder="e.g., 6">
    </div>
    
    <button type="submit" class="btn btn-primary">Check Eligibility</button>
</form>

<div id="eligibility-result" class="result-box" style="display: none;">
    <!-- Results will be displayed here -->
</div>

<script>
async function checkEligibility(event) {
    event.preventDefault();
    
    const formData = {
        employment_type: document.getElementById('employment_type').value,
        hours_per_week: parseInt(document.getElementById('hours_per_week').value),
        tenure_months: parseInt(document.getElementById('tenure_months').value)
    };
    
    const resultBox = document.getElementById('eligibility-result');
    resultBox.style.display = 'block';
    resultBox.innerHTML = '<p>Checking eligibility...</p>';
    
    try {
        const response = await fetch('/api/eligibility', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.eligible) {
            resultBox.className = 'result-box success';
            resultBox.innerHTML = `
                <h3>✓ You are eligible for benefits!</h3>
                <p>${result.reason}</p>
                <p>You qualify for ${result.benefits.length} benefit(s).</p>
                <a href="/benefits" class="btn btn-primary">View Available Benefits</a>
            `;
        } else {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = `
                <h3>✗ Not currently eligible</h3>
                <p>${result.reason}</p>
                <p>Contact HR if you have questions about your eligibility status.</p>
            `;
        }
    } catch (error) {
        resultBox.className = 'result-box error';
        resultBox.innerHTML = '<p class="error">Failed to check eligibility. Please try again.</p>';
    }
    
    return false;
}
</script>
{% endblock %}
'''

    def _generate_contact_page(self) -> str:
        """Generate contact form page template."""
        return '''{% extends "base.html" %}

{% block title %}Contact Us - Employee Benefits Portal{% endblock %}

{% block content %}
<h1>Contact HR Support</h1>
<p class="page-intro">Have questions about your benefits? We're here to help.</p>

<form id="contact-form" class="form" onsubmit="return submitContact(event)">
    <div class="form-group">
        <label for="name">Your Name *</label>
        <input type="text" id="name" name="name" required 
               maxlength="200" placeholder="John Doe">
    </div>
    
    <div class="form-group">
        <label for="email">Email Address *</label>
        <input type="email" id="email" name="email" required 
               maxlength="200" placeholder="john.doe@example.com">
    </div>
    
    <div class="form-group">
        <label for="subject">Subject *</label>
        <input type="text" id="subject" name="subject" required 
               maxlength="500" placeholder="Question about health insurance">
    </div>
    
    <div class="form-group">
        <label for="message">Message *</label>
        <textarea id="message" name="message" required 
                  maxlength="5000" rows="6" 
                  placeholder="Please describe your question or concern..."></textarea>
    </div>
    
    <button type="submit" class="btn btn-primary">Submit Message</button>
</form>

<div id="contact-result" class="result-box" style="display: none;">
    <!-- Result will be displayed here -->
</div>

<script>
async function submitContact(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        subject: document.getElementById('subject').value,
        message: document.getElementById('message').value
    };
    
    const resultBox = document.getElementById('contact-result');
    resultBox.style.display = 'block';
    resultBox.innerHTML = '<p>Submitting your message...</p>';
    
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            resultBox.className = 'result-box success';
            resultBox.innerHTML = `
                <h3>✓ Message Sent!</h3>
                <p>${result.message}</p>
                <p>Reference ID: ${result.message_id}</p>
                <p>We'll respond to your email within 2 business days.</p>
            `;
            document.getElementById('contact-form').reset();
        } else {
            throw new Error(result.detail || 'Submission failed');
        }
    } catch (error) {
        resultBox.className = 'result-box error';
        resultBox.innerHTML = `<p class="error">Failed to send message: ${error.message}. Please try again.</p>`;
    }
    
    return false;
}
</script>
{% endblock %}
'''

    def _generate_admin_page(self) -> str:
        """Generate admin page template."""
        return '''{% extends "base.html" %}

{% block title %}Admin - Employee Benefits Portal{% endblock %}

{% block content %}
<h1>Admin Dashboard</h1>
<p class="page-intro">View submitted contact messages and system information.</p>

<section class="admin-section">
    <h2>Contact Messages</h2>
    <div id="messages-list" class="messages-table">
        <!-- Messages will be loaded dynamically -->
        <div class="loading">Loading messages...</div>
    </div>
</section>

<section class="admin-section">
    <h2>System Information</h2>
    <div class="info-card">
        <p><strong>Application:</strong> Employee Benefits Portal v1.0.0</p>
        <p><strong>Framework:</strong> FastAPI + Jinja2</p>
        <p><strong>Database:</strong> SQLite</p>
        <p><strong>Note:</strong> This is a demo application using synthetic data only.</p>
    </div>
</section>

<script>
async function loadMessages() {
    try {
        const response = await fetch('/api/admin/messages');
        const messages = await response.json();
        
        const container = document.getElementById('messages-list');
        if (messages.length === 0) {
            container.innerHTML = '<p>No messages yet.</p>';
            return;
        }
        
        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Subject</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${messages.map(msg => `
                        <tr>
                            <td>${new Date(msg.created_at).toLocaleDateString()}</td>
                            <td>${msg.name}</td>
                            <td>${msg.email}</td>
                            <td>${msg.subject}</td>
                            <td>${msg.is_read ? 'Read' : 'Unread'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        document.getElementById('messages-list').innerHTML = 
            '<p class="error">Failed to load messages.</p>';
    }
}
loadMessages();
</script>
{% endblock %}
'''

    def _generate_css(self) -> str:
        """Generate CSS stylesheet."""
        return '''/* Employee Benefits Portal Styles */

/* CSS Variables */
:root {
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    --success-color: #22c55e;
    --error-color: #ef4444;
    --background: #f8fafc;
    --surface: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}

/* Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.main {
    min-height: calc(100vh - 300px);
    padding: 2rem 0;
}

/* Header & Navigation */
.header {
    background: var(--surface);
    border-bottom: 1px solid var(--border-color);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 1.5rem;
}

.nav-menu a {
    color: var(--text-primary);
    text-decoration: none;
    transition: color 0.2s;
}

.nav-menu a:hover {
    color: var(--primary-color);
}

.admin-link {
    color: var(--secondary-color) !important;
}

.nav-toggle {
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
}

.nav-toggle span {
    width: 24px;
    height: 2px;
    background: var(--text-primary);
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    margin-bottom: 2rem;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
}

.btn-secondary {
    background: white;
    color: var(--primary-color);
}

.btn-secondary:hover {
    background: var(--background);
}

/* Feature Grid */
.features {
    padding: 2rem 0;
}

.features h2 {
    text-align: center;
    margin-bottom: 2rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.feature-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow);
}

.feature-card h3 {
    margin-bottom: 0.5rem;
    color: var(--primary-color);
}

.feature-card a {
    color: var(--primary-color);
    text-decoration: none;
}

/* Benefits Grid */
.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.benefit-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--primary-color);
}

.benefit-category {
    display: inline-block;
    background: var(--primary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    margin-bottom: 0.5rem;
}

/* FAQs */
.search-box {
    margin: 1.5rem 0;
}

.search-box input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    font-size: 1rem;
}

.faqs-list {
    margin-top: 1.5rem;
}

.faq-item {
    background: var(--surface);
    margin-bottom: 0.5rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow);
}

.faq-item summary {
    padding: 1rem 1.5rem;
    cursor: pointer;
    font-weight: 500;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.faq-item summary::after {
    content: '+';
    font-size: 1.5rem;
}

.faq-item[open] summary::after {
    content: '-';
}

.faq-item p {
    padding: 0 1.5rem 1.5rem;
    color: var(--text-secondary);
}

/* Forms */
.form {
    max-width: 600px;
    background: var(--surface);
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Result Boxes */
.result-box {
    max-width: 600px;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-top: 1.5rem;
}

.result-box.success {
    background: #dcfce7;
    border: 1px solid var(--success-color);
}

.result-box.error {
    background: #fee2e2;
    border: 1px solid var(--error-color);
}

/* Admin */
.admin-section {
    margin-bottom: 2rem;
}

.messages-table table {
    width: 100%;
    background: var(--surface);
    border-collapse: collapse;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.messages-table th,
.messages-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.messages-table th {
    background: var(--background);
    font-weight: 600;
}

.info-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: var(--shadow);
}

/* Footer */
.footer {
    background: var(--text-primary);
    color: white;
    padding: 2rem 0;
    text-align: center;
}

.disclaimer {
    font-size: 0.875rem;
    opacity: 0.7;
    margin-top: 0.5rem;
}

/* Utilities */
.loading {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary);
}

.error {
    color: var(--error-color);
}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--surface);
        flex-direction: column;
        padding: 1rem;
        box-shadow: var(--shadow-lg);
    }
    
    .nav-menu.active {
        display: flex;
    }
    
    .nav-toggle {
        display: flex;
    }
    
    .hero h1 {
        font-size: 1.75rem;
    }
    
    .hero-actions {
        flex-direction: column;
    }
    
    .feature-grid,
    .benefits-grid {
        grid-template-columns: 1fr;
    }
}

/* Print styles */
@media print {
    .header,
    .footer,
    .nav-toggle {
        display: none;
    }
}
'''
