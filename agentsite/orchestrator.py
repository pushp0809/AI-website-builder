"""Main orchestrator for AgentSite pipeline."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from agentsite.agents.registry import initialize_registry, AgentRegistry
from agentsite.artifact_store import ArtifactStore
from agentsite.state_manager import StateManager, TaskStatus, PhaseStatus
from agentsite.task_manager import TaskManager
from agentsite.llm_client import get_llm_client
from agentsite.validation_gates import ValidationGates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates the multi-agent website building pipeline."""

    def __init__(self):
        # Initialize registry
        initialize_registry()
        
        self.state_manager = StateManager()
        self.task_manager = TaskManager()
        self.artifact_store = ArtifactStore()
        self.gates = ValidationGates(self.artifact_store, self.state_manager)
        self.llm_client = get_llm_client()
        
        self.pipeline_phases = [
            "requirements",
            "design",
            "api_spec",
            "database",
            "frontend",
            "backend",
            "integration",
            "testing",
            "security",
            "documentation",
            "final_review",
        ]

    def run(self, requirement: str) -> dict[str, Any]:
        """Run the complete pipeline with the given requirement."""
        logger.info(f"Starting pipeline with requirement: {requirement[:100]}...")
        
        self.state_manager.set_requirement(requirement)
        
        try:
            # Phase 1: Requirements
            if not self._run_requirements_phase(requirement):
                return self._fail_pipeline("Requirements phase failed")
            
            # Phase 2: Design
            if not self._run_design_phase():
                return self._fail_pipeline("Design phase failed")
            
            # Phase 3: API Spec
            if not self._run_api_spec_phase():
                return self._fail_pipeline("API spec phase failed")
            
            # Phase 4: Database
            if not self._run_database_phase():
                return self._fail_pipeline("Database phase failed")
            
            # Phase 5: Frontend
            if not self._run_frontend_phase():
                return self._fail_pipeline("Frontend phase failed")
            
            # Phase 6: Backend
            if not self._run_backend_phase():
                return self._fail_pipeline("Backend phase failed")
            
            # Phase 7: Integration
            if not self._run_integration_phase():
                return self._fail_pipeline("Integration phase failed")
            
            # Phase 8: Testing
            if not self._run_testing_phase():
                logger.warning("Testing phase had issues but continuing...")
            
            # Phase 9: Security
            if not self._run_security_phase():
                logger.warning("Security phase had issues but continuing...")
            
            # Phase 10: Documentation
            if not self._run_documentation_phase():
                logger.warning("Documentation phase had issues but continuing...")
            
            # Phase 11: Final Review
            if not self._run_final_review():
                return self._fail_pipeline("Final review failed")
            
            # Success!
            self.state_manager.complete_pipeline(success=True)
            logger.info("Pipeline completed successfully!")
            
            return {
                "success": True,
                "message": "Pipeline completed successfully",
                "state": self.state_manager.get_state(),
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed with error: {e}")
            return self._fail_pipeline(str(e))

    def _fail_pipeline(self, reason: str) -> dict[str, Any]:
        """Mark pipeline as failed."""
        self.state_manager.complete_pipeline(success=False, error_message=reason)
        return {
            "success": False,
            "message": reason,
            "state": self.state_manager.get_state(),
        }

    def _run_requirements_phase(self, requirement: str) -> bool:
        """Run requirements gathering phase."""
        logger.info("Phase 1: Requirements")
        self.state_manager.set_current_phase("requirements")
        
        # Create ProductAgent task
        agent = AgentRegistry.create_agent("ProductAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="req_001",
            phase="requirements",
            assigned_agent="ProductAgent",
            goal="Generate PRD, user stories, and assumptions",
            inputs={"requirement": requirement},
            definition_of_done="PRD, user stories, and assumptions documents created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({"requirement": requirement})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            # Run gate check
            gate_passed = self.gates.check_requirements_gate()
            self.state_manager.record_gate("requirements", gate_passed)
            
            if gate_passed:
                self.state_manager.complete_phase("requirements")
                return True
            else:
                self.state_manager.fail_phase("requirements", "Requirements gate failed")
                return False
                
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_design_phase(self) -> bool:
        """Run design phase."""
        logger.info("Phase 2: Design")
        self.state_manager.set_current_phase("design")
        
        agent = AgentRegistry.create_agent("DesignAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="design_001",
            phase="design",
            assigned_agent="DesignAgent",
            goal="Generate sitemap, design spec, and architecture",
            inputs={},
            definition_of_done="Sitemap, design spec, and architecture documents created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            gate_passed = self.gates.check_design_gate()
            self.state_manager.record_gate("design", gate_passed)
            
            if gate_passed:
                self.state_manager.complete_phase("design")
                return True
            else:
                self.state_manager.fail_phase("design", "Design gate failed")
                return False
                
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_api_spec_phase(self) -> bool:
        """Run API specification phase."""
        logger.info("Phase 3: API Specification")
        self.state_manager.set_current_phase("api_spec")
        
        agent = AgentRegistry.create_agent("APISpecAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="api_001",
            phase="api_spec",
            assigned_agent="APISpecAgent",
            goal="Generate OpenAPI specification",
            inputs={},
            definition_of_done="API specification document created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("api_spec")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_database_phase(self) -> bool:
        """Run database design phase."""
        logger.info("Phase 4: Database")
        self.state_manager.set_current_phase("database")
        
        agent = AgentRegistry.create_agent("DatabaseAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="db_001",
            phase="database",
            assigned_agent="DatabaseAgent",
            goal="Generate database schema, models, and seed data",
            inputs={},
            definition_of_done="Database schema, models, and seed data created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("database")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_frontend_phase(self) -> bool:
        """Run frontend generation phase."""
        logger.info("Phase 5: Frontend")
        self.state_manager.set_current_phase("frontend")
        
        agent = AgentRegistry.create_agent("FrontendAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="fe_001",
            phase="frontend",
            assigned_agent="FrontendAgent",
            goal="Generate HTML templates and CSS",
            inputs={},
            definition_of_done="All page templates and stylesheets created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("frontend")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_backend_phase(self) -> bool:
        """Run backend generation phase."""
        logger.info("Phase 6: Backend")
        self.state_manager.set_current_phase("backend")
        
        agent = AgentRegistry.create_agent("BackendAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="be_001",
            phase="backend",
            assigned_agent="BackendAgent",
            goal="Generate FastAPI application code",
            inputs={},
            definition_of_done="FastAPI app, routes, and schemas created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("backend")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_integration_phase(self) -> bool:
        """Run integration phase."""
        logger.info("Phase 7: Integration")
        self.state_manager.set_current_phase("integration")
        
        agent = AgentRegistry.create_agent("IntegrationAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="int_001",
            phase="integration",
            assigned_agent="IntegrationAgent",
            goal="Create integration scripts and assemble application",
            inputs={},
            definition_of_done="Application assembled and integration tests created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("integration")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_testing_phase(self) -> bool:
        """Run testing phase."""
        logger.info("Phase 8: Testing")
        self.state_manager.set_current_phase("testing")
        
        agent = AgentRegistry.create_agent("QAValidatorAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="qa_001",
            phase="testing",
            assigned_agent="QAValidatorAgent",
            goal="Run integration tests and generate test report",
            inputs={},
            definition_of_done="Test report generated",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            gate_passed = result.get("success", False)
            self.state_manager.record_gate("testing", gate_passed, {"test_results": result})
            
            self.state_manager.complete_phase("testing", gate_passed)
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_security_phase(self) -> bool:
        """Run security audit phase."""
        logger.info("Phase 9: Security Audit")
        self.state_manager.set_current_phase("security")
        
        agent = AgentRegistry.create_agent("SecurityAuditorAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="sec_001",
            phase="security",
            assigned_agent="SecurityAuditorAgent",
            goal="Run security audit and generate security report",
            inputs={},
            definition_of_done="Security report generated",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            gate_passed = result.get("passed", False)
            self.state_manager.record_gate("security", gate_passed, {"findings": result.get("findings", [])})
            
            self.state_manager.complete_phase("security", gate_passed)
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_documentation_phase(self) -> bool:
        """Run documentation phase."""
        logger.info("Phase 10: Documentation")
        self.state_manager.set_current_phase("documentation")
        
        agent = AgentRegistry.create_agent("DocumentationAgent", artifact_store=self.artifact_store)
        task = self.task_manager.create_task(
            task_id="doc_001",
            phase="documentation",
            assigned_agent="DocumentationAgent",
            goal="Generate README, security docs, and demo script",
            inputs={},
            definition_of_done="Documentation files created",
        )
        
        self.task_manager.update_status(task["task_id"], TaskStatus.IN_PROGRESS)
        
        try:
            result = agent.execute({})
            self.task_manager.set_result(task["task_id"], result.get("summary", ""), result.get("artifacts", []))
            self.task_manager.update_status(task["task_id"], TaskStatus.COMPLETED)
            
            self.state_manager.complete_phase("documentation")
            return True
        except Exception as e:
            self.task_manager.add_error(task["task_id"], str(e))
            self.task_manager.update_status(task["task_id"], TaskStatus.FAILED)
            return False

    def _run_final_review(self) -> bool:
        """Run final review phase."""
        logger.info("Phase 11: Final Review")
        self.state_manager.set_current_phase("final_review")
        
        # Check all required artifacts exist
        missing = self.artifact_store.get_missing_artifacts()
        if missing:
            logger.warning(f"Missing artifacts: {missing}")
        
        # Generate final execution report
        self._generate_execution_report()
        
        self.state_manager.complete_phase("final_review")
        return True

    def _generate_execution_report(self) -> str:
        """Generate final execution report."""
        state = self.state_manager.get_state()
        
        report = f"""# Execution Report

## Pipeline Summary

**Pipeline ID:** {state['pipeline_id']}
**Requirement:** {state['requirement']}
**Status:** {state['final_status']}
**Started:** {state['started_at']}
**Completed:** {state.get('completed_at', 'N/A')}

## Phases Executed

"""
        for phase_name, phase_data in state.get('phases', {}).items():
            status = phase_data.get('status', 'UNKNOWN')
            gate = phase_data.get('gate_status', 'N/A')
            report += f"- **{phase_name}**: {status} (Gate: {gate})\n"
        
        report += f"""
## Metrics

- Total Tasks: {state['metrics']['total_tasks']}
- Completed: {state['metrics']['completed_tasks']}
- Failed: {state['metrics']['failed_tasks']}
- Blocked: {state['metrics']['blocked_tasks']}

## Artifacts Generated

"""
        for artifact in state.get('artifacts_generated', []):
            report += f"- {artifact}\n"
        
        report += """
## Gates Passed

"""
        for gate_name, gate_result in state.get('gates', {}).items():
            status = "✓" if gate_result.get('passed') else "✗"
            report += f"- {status} {gate_name}\n"
        
        # Save report
        from pathlib import Path
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        report_path = reports_dir / f"execution_{state['pipeline_id']}.md"
        
        with open(report_path, "w") as f:
            f.write(report)
        
        logger.info(f"Execution report saved to {report_path}")
        return report
