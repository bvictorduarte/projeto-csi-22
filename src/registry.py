from typing import Dict, Type
from src.handlers.base_handler import Handler
from src.agents.base_agent import Agent, OpenAIAgent

# Imports dos handlers
from src.handlers.router.handler import RouterHandler
from src.handlers.fundamentos.handler import FundamentosHandler
from src.handlers.design_patterns.handler import DesignPatternsHandler
from src.handlers.especifico_materia.handler import EspecificoMateriaHandler

# Imports dos prompts e configs
from src.agents.router.prompt import ROUTER_PROMPT
from src.agents.router.config import ROUTER_CONFIG

from src.agents.fundamentos.prompt import FUNDAMENTOS_PROMPT
from src.agents.fundamentos.config import FUNDAMENTOS_CONFIG

from src.agents.design_patterns.prompt import DESIGN_PATTERNS_PROMPT
from src.agents.design_patterns.config import DESIGN_PATTERNS_CONFIG

from src.agents.especifico_materia.prompt import ESPECIFICO_MATERIA_PROMPT
from src.agents.especifico_materia.config import ESPECIFICO_MATERIA_CONFIG

class Registry:
    def __init__(self):
        # Mapeamento de nomes para classes de handlers
        self.handler_types: Dict[str, Type[Handler]] = {
            "router": RouterHandler,
            "fundamentos_poo": FundamentosHandler,
            "design_patterns": DesignPatternsHandler,
            "especifico_materia": EspecificoMateriaHandler
        }

        # Mapeamento de nomes para configurações de agents
        self.agent_configs = {
            "router": (ROUTER_CONFIG, ROUTER_PROMPT),
            "fundamentos_poo": (FUNDAMENTOS_CONFIG, FUNDAMENTOS_PROMPT),
            "design_patterns": (DESIGN_PATTERNS_CONFIG, DESIGN_PATTERNS_PROMPT),
            "especifico_materia": (ESPECIFICO_MATERIA_CONFIG, ESPECIFICO_MATERIA_PROMPT)
        }

    def create_handler(self, handler_type: str) -> Handler:
        """
        Cria um handler do tipo especificado com seu agent correspondente.
        """
        if handler_type not in self.handler_types or handler_type not in self.agent_configs:
            raise ValueError(f"Tipo de handler não registrado: {handler_type}")

        # Cria o agent
        config, prompt = self.agent_configs[handler_type]
        agent = OpenAIAgent(config=config, system_prompt=prompt)

        # Cria e retorna o handler
        handler_class = self.handler_types[handler_type]
        return handler_class(agent=agent) 