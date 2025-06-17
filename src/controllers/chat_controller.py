from typing import List, Dict
from src.handlers.base_handler import Handler
from src.agents.base_agent import HandlerType
from src.registry import Registry

class ChatController:
    def __init__(self):
        self.registry = Registry()
        self.handlers: Dict[str, Handler] = {}

    def get_handler(self, handler_type: str) -> Handler:
        """
        Obtém um handler existente ou cria um novo se necessário.
        """
        if handler_type not in self.handlers:
            self.handlers[handler_type] = self.registry.create_handler(handler_type)
        return self.handlers[handler_type]

    async def process_message(self, context: List[str]) -> str:
        """
        Processa a mensagem através dos handlers até receber uma resposta final.
        """
        current_handler = "router"
        
        while True:
            handler = self.get_handler(current_handler)
            response = await handler.handle(context)
            
            if response.handler_type == HandlerType.FINAL:
                return response.message
            
            current_handler = response.next_handler 