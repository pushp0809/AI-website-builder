"""API Spec Generator - Creates API specification."""

from typing import Any

from agentsite.agents.base_agent import BaseAgent
from agentsite.agents.registry import AgentRegistry


@AgentRegistry.register
class APISpecAgent(BaseAgent):
    """Creates API specification document."""

    name = "APISpecAgent"
    role = "API Architect"
    system_prompt = """You are an expert API Architect AI agent.
Create a comprehensive API specification using YAML format.
Include all endpoints, request/response schemas, and error handling."""

    input_artifacts = ["01_prd.md", "03_sitemap.md"]
    output_artifacts = ["05_api_spec.yaml"]
    allowed_tools = ["file_read", "file_write"]

    def execute(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """Execute API spec generation task."""
        api_spec = """openapi: 3.0.3
info:
  title: Employee Benefits Portal API
  description: API for the Employee Benefits Information Portal
  version: 1.0.0

servers:
  - url: http://localhost:8000
    description: Local development server

paths:
  /api/benefits:
    get:
      summary: Get all benefits
      operationId: get_benefits
      tags: [Benefits]
      responses:
        '200':
          description: List of benefits
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Benefit'

  /api/faqs:
    get:
      summary: Get all FAQs
      operationId: get_faqs
      tags: [FAQs]
      responses:
        '200':
          description: List of FAQs
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/FAQ'

  /api/eligibility:
    post:
      summary: Check eligibility for benefits
      operationId: check_eligibility
      tags: [Eligibility]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EligibilityRequest'
      responses:
        '200':
          description: Eligibility result
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EligibilityResponse'
        '400':
          description: Invalid request

  /api/contact:
    post:
      summary: Submit contact message
      operationId: submit_contact
      tags: [Contact]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ContactRequest'
      responses:
        '200':
          description: Message submitted successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ContactResponse'
        '400':
          description: Invalid request

  /api/admin/messages:
    get:
      summary: Get all contact messages (admin)
      operationId: get_messages
      tags: [Admin]
      responses:
        '200':
          description: List of messages
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ContactMessage'

components:
  schemas:
    Benefit:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        category:
          type: string
        eligibility_requirements:
          type: string

    FAQ:
      type: object
      properties:
        id:
          type: integer
        question:
          type: string
        answer:
          type: string
        category:
          type: string

    EligibilityRequest:
      type: object
      required:
        - employment_type
        - hours_per_week
        - tenure_months
      properties:
        employment_type:
          type: string
          enum: [full-time, part-time, contractor]
        hours_per_week:
          type: integer
          minimum: 0
        tenure_months:
          type: integer
          minimum: 0

    EligibilityResponse:
      type: object
      properties:
        eligible:
          type: boolean
        benefits:
          type: array
          items:
            $ref: '#/components/schemas/Benefit'
        reason:
          type: string

    ContactRequest:
      type: object
      required:
        - name
        - email
        - subject
        - message
      properties:
        name:
          type: string
          maxLength: 200
        email:
          type: string
          format: email
        subject:
          type: string
          maxLength: 500
        message:
          type: string
          maxLength: 5000

    ContactResponse:
      type: object
      properties:
        success:
          type: boolean
        message_id:
          type: integer
        message:
          type: string

    ContactMessage:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
        subject:
          type: string
        message:
          type: string
        is_read:
          type: boolean
        created_at:
          type: string
          format: date-time
"""
        spec_path = self.artifact_store.save("05_api_spec.yaml", api_spec)
        return {
            "success": True,
            "artifacts": [spec_path],
            "summary": "Generated API specification",
        }
