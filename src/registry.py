from typing import Dict, Type, Tuple, Optional
from src.handlers.base_handler import Handler
from src.agents.base_agent import Agent, OpenAIAgent
from src.utils.exceptions import HandlerNotFoundError, AgentConfigurationError
from src.utils.logger import get_logger

# Imports dos handlers
from src.handlers.router.handler import RouterHandler
from src.handlers.conteudo_materia.handler import ConteudoMateriaHandler

# Imports dos prompts e configs
from src.agents.router.prompt import ROUTER_PROMPT
from src.agents.router.config import ROUTER_CONFIG

from src.agents.conteudo_materia.prompt import CONTEUDO_MATERIA_PROMPT
from src.agents.conteudo_materia.config import config as CONTEUDO_MATERIA_CONFIG

class Registry:
    """
    Registro central para handlers e agents do POO Chat.
    Implementa o padrão Singleton para garantir uma única instância do registro.
    
    Attributes:
        _instance: Instância única da classe
        handler_types: Mapeamento de nomes para classes de handlers
        agent_configs: Mapeamento de nomes para configurações de agents
    """
    
    _instance: Optional['Registry'] = None
    
    def __new__(cls) -> 'Registry':
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.logger = get_logger(__name__)
        
        # Mapeamento de nomes para classes de handlers
        self.handler_types: Dict[str, Type[Handler]] = {
            "router": RouterHandler,
            "conteudo_materia": ConteudoMateriaHandler
        }

        # Mapeamento de nomes para configurações de agents
        self.agent_configs: Dict[str, Tuple] = {
            "router": (ROUTER_CONFIG, ROUTER_PROMPT),
            "conteudo_materia": (CONTEUDO_MATERIA_CONFIG, CONTEUDO_MATERIA_PROMPT)
        }
        
        self._initialized = True
        self.logger.info("Registry inicializado com sucesso")

    def create_handler(self, handler_type: str) -> Handler:
        """
        Cria um handler do tipo especificado com seu agent correspondente.
        
        Args:
            handler_type: Tipo do handler a ser criado
            
        Returns:
            Handler: Nova instância do handler solicitado
            
        Raises:
            HandlerNotFoundError: Se o tipo de handler não estiver registrado
            AgentConfigurationError: Se houver erro na configuração do agent
        """
        try:
            if handler_type not in self.handler_types:
                raise HandlerNotFoundError(f"Tipo de handler não registrado: {handler_type}")

            if handler_type not in self.agent_configs:
                raise AgentConfigurationError(f"Configuração de agent não encontrada: {handler_type}")

            # Cria o agent
            config, prompt = self.agent_configs[handler_type]
            agent = OpenAIAgent(config=config, system_prompt=prompt)

            # Cria e retorna o handler
            handler_class = self.handler_types[handler_type]
            handler = handler_class(agent=agent)
            
            return handler
            
        except Exception as e:
            self.logger.error(f"Erro ao criar handler '{handler_type}': {str(e)}")
            raise 