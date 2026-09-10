"""Agent registry for managing specialist agents."""

from typing import Type

from agentsite.agents.base_agent import BaseAgent


class AgentRegistry:
    """Registry for all specialist agents."""

    _agents: dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, agent_class: Type[BaseAgent]) -> Type[BaseAgent]:
        """Register an agent class."""
        cls._agents[agent_class.name] = agent_class
        return agent_class

    @classmethod
    def get_agent(cls, name: str) -> Type[BaseAgent] | None:
        """Get an agent class by name."""
        return cls._agents.get(name)

    @classmethod
    def create_agent(cls, name: str, **kwargs):
        """Create an instance of an agent."""
        agent_class = cls.get_agent(name)
        if not agent_class:
            raise ValueError(f"Unknown agent: {name}")
        return agent_class(**kwargs)

    @classmethod
    def list_agents(cls) -> list[str]:
        """List all registered agent names."""
        return list(cls._agents.keys())

    @classmethod
    def get_all_agents(cls) -> dict[str, Type[BaseAgent]]:
        """Get all registered agents."""
        return cls._agents.copy()


# Import all agent modules to register them
# This must be at the end to avoid circular imports
def initialize_registry():
    """Initialize the agent registry with all agents."""
    from agentsite.agents.product_agent import ProductAgent
    from agentsite.agents.design_agent import DesignAgent
    from agentsite.agents.frontend_agent import FrontendAgent
    from agentsite.agents.backend_agent import BackendAgent
    from agentsite.agents.database_agent import DatabaseAgent
    from agentsite.agents.integration_agent import IntegrationAgent
    from agentsite.agents.qa_validator_agent import QAValidatorAgent
    from agentsite.agents.security_auditor_agent import SecurityAuditorAgent
    from agentsite.agents.documentation_agent import DocumentationAgent
    from agentsite.agents.critic_agent import CriticAgent
    from agentsite.agents.api_spec_agent import APISpecAgent

    AgentRegistry.register(ProductAgent)
    AgentRegistry.register(DesignAgent)
    AgentRegistry.register(FrontendAgent)
    AgentRegistry.register(BackendAgent)
    AgentRegistry.register(DatabaseAgent)
    AgentRegistry.register(IntegrationAgent)
    AgentRegistry.register(QAValidatorAgent)
    AgentRegistry.register(SecurityAuditorAgent)
    AgentRegistry.register(DocumentationAgent)
    AgentRegistry.register(CriticAgent)
    AgentRegistry.register(APISpecAgent)
