from dataclasses import dataclass
from typing import Optional, List

@dataclass
class HandlerResponse:
    message: str
    next_handler: Optional[str] = None

class POOHandler:
    def __init__(self):
        """
        Inicializa o handler base para processamento de mensagens relacionadas a POO.
        A implementação completa será feita nas próximas etapas.
        """
        pass

    def route_message(self, messages: List[str]) -> str:
        """
        Determina qual fluxo seguir com base nas mensagens.
        Será implementado posteriormente.
        """
        pass

    def handle_message(self, flow: str, messages: List[str]) -> HandlerResponse:
        """
        Processa a mensagem de acordo com o fluxo determinado.
        Será implementado posteriormente.
        """
        pass 