from typing import List
from src.agents.base_agent import AgentResponse, HandlerType
from src.handlers.base_handler import Handler
from src.utils.logger import get_logger

class RouterHandler(Handler):
    """
    Handler responsável por rotear mensagens para os handlers apropriados.
    """
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = get_logger(__name__)
        self.current_handler = None
        
    async def handle(self, context: List[str]) -> AgentResponse:
        """
        Processa a mensagem e determina qual handler deve processá-la,
        considerando todo o contexto da conversa.
        """
        try:
            # Se já tivermos um handler atual e a mensagem for de continuação,
            # mantemos o mesmo handler
            if self.current_handler and self._is_follow_up_question(context[-1]):
                return AgentResponse(
                    handler_type=HandlerType.NEXT,
                    next_handler=self.current_handler
                )
            
            # Caso contrário, consultamos o agente para determinar o handler
            response = await self.agent.process(context)
            
            # Armazenamos o handler escolhido
            if response.handler_type == HandlerType.NEXT:
                self.current_handler = response.next_handler
            elif response.message:
                self.current_handler = response.message.strip()
            else:
                self.current_handler = "fundamentos_poo"
            
            # Garante que a resposta do router é sempre do tipo NEXT
            return AgentResponse(
                handler_type=HandlerType.NEXT,
                next_handler=self.current_handler
            )
                
        except Exception as e:
            self.logger.error(f"Erro no RouterHandler: {str(e)}")
            # Em caso de erro, retorna para o handler padrão
            self.current_handler = "fundamentos_poo"
            return AgentResponse(
                handler_type=HandlerType.NEXT,
                next_handler=self.current_handler
            )
    
    def _is_follow_up_question(self, message: str) -> bool:
        """
        Verifica se a mensagem parece ser uma pergunta de continuação
        do mesmo assunto.
        """
        follow_up_indicators = [
            "como", "pode", "exemplo", "explique", "mostre",
            "e se", "então", "mas", "e", "também",
            "mais detalhes", "melhor", "por que",
            "?", "..."
        ]
        
        message = message.lower().strip()
        return any(indicator in message for indicator in follow_up_indicators) 