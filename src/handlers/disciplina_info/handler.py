from typing import List
from src.agents.base_agent import AgentResponse, HandlerType
from src.handlers.base_handler import Handler
from src.utils.logger import get_logger

class DisciplinaInfoHandler(Handler):
    """
    Handler responsável por processar mensagens relacionadas a informações
    específicas sobre a disciplina CSI22, incluindo horários, professora,
    projetos, laboratórios e outros detalhes administrativos.
    """
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = get_logger(__name__)
        
    async def handle(self, context: List[str]) -> AgentResponse:
        """
        Processa a mensagem considerando o contexto da conversa e retorna
        informações específicas sobre a disciplina CSI22.
        """
        try:
            response = await self.agent.process(context)
            return response
            
        except Exception as e:
            return AgentResponse(
                handler_type=HandlerType.FINAL,
                message="Desculpe, ocorreu um erro ao processar sua pergunta sobre a disciplina. "
                       "Pode reformular a pergunta?"
            ) 