from typing import List
from src.agents.base_agent import AgentResponse, HandlerType
from src.handlers.base_handler import Handler
from src.utils.logger import get_logger

class ProjetoJogoHandler(Handler):
    """
    Handler responsável por processar mensagens relacionadas ao Projeto 1 da disciplina CSI22,
    cujo objetivo é o desenvolvimento de um jogo em Python utilizando Pygame. 
    Esse handler trata questões sobre estrutura de código, uso de POO, organização do projeto,
    funcionalidades, documentação (GDD), vídeo e apresentação final.
    """

    def __init__(self, agent):
        super().__init__(agent)
        self.logger = get_logger(__name__)
        
    async def handle(self, context: List[str]) -> AgentResponse:
        """
        Processa a mensagem considerando o contexto da conversa e retorna
        informações específicas sobre o Projeto 1 da disciplina CSI22.
        """
        try:
            response = await self.agent.process(context)
            return response

        except Exception as e:
            self.logger.error(f"Erro no ProjetoJogoHandler: {e}")
            return AgentResponse(
                handler_type=HandlerType.FINAL,
                message="Desculpe, ocorreu um erro ao processar sua dúvida sobre o Projeto 1. "
                        "Você pode reformular a pergunta ou tentar novamente?"
            )
