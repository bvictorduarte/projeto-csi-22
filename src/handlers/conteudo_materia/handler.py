from typing import List
from src.agents.base_agent import AgentResponse, HandlerType
from src.handlers.base_handler import Handler
from src.utils.logger import get_logger

class ConteudoMateriaHandler(Handler):
    """
    Handler responsável por processar mensagens relacionadas aos conteúdos
    específicos da matéria, incluindo histórico de perguntas e respostas.
    """
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = get_logger(__name__)
        
    async def handle(self, context: List[str]) -> AgentResponse:
        """
        Processa a mensagem considerando o contexto da conversa e o histórico
        de perguntas e respostas sobre o conteúdo da matéria.
        """
        try:
            # Processa a mensagem com o agente
            response = await self.agent.process(context)
            
            # Registra a resposta para debug
            self.logger.info(
                f"Processada mensagem sobre conteúdo da matéria: {context[-1]}"
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Erro no ConteudoMateriaHandler: {str(e)}")
            return AgentResponse(
                handler_type=HandlerType.FINAL,
                message="Desculpe, ocorreu um erro ao processar sua mensagem sobre o conteúdo. "
                       "Pode reformular a pergunta?"
            ) 