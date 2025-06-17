from src.agents.base_agent import AgentConfig

ROUTER_CONFIG = AgentConfig(
    model="gpt-3.5-turbo",
    temperature=0.3  # Temperatura mais baixa para decisões mais consistentes
) 