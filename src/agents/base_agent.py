from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import openai
import os
from src.utils.logger import get_logger

class HandlerType(Enum):
    NEXT = "next"
    FINAL = "final"

@dataclass
class AgentResponse:
    handler_type: HandlerType
    next_handler: Optional[str] = None
    message: Optional[str] = None

@dataclass
class AgentConfig:
    model: str
    temperature: float
    max_tokens: int

class Agent(ABC):
    def __init__(self, config: AgentConfig, system_prompt: str):
        self.config = config
        self.system_prompt = system_prompt
        self.logger = get_logger(__name__)

    @abstractmethod
    async def process(self, context: list[str]) -> AgentResponse:
        """Processa o contexto e retorna uma resposta."""
        pass

class OpenAIAgent(Agent):
    def __init__(self, config: AgentConfig, system_prompt: str):
        super().__init__(config, system_prompt)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente!")
        openai.api_key = api_key

    async def process(self, context: list[str]) -> AgentResponse:
        """
        Processa o contexto usando a API da OpenAI.
        
        Args:
            context: Lista de mensagens do histórico da conversa
            
        Returns:
            AgentResponse: Resposta do agente contendo o tipo de handler e a mensagem/próximo handler
            
        Raises:
            openai.error.OpenAIError: Se houver erro na comunicação com a API
        """
        if not context:
            raise ValueError("Contexto vazio não é permitido")
            
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context[-1]}  # Última mensagem do contexto
                ]
            )

            content = response.choices[0].message.content.strip()

            # Se for o router, a resposta deve ser um dos handlers válidos
            if "router" in self.system_prompt.lower():
                valid_handlers = ["conteudo_materia"]
                # Verifica se o conteúdo corresponde a um handler válido
                handler = content.lower().strip()
                if handler in valid_handlers:
                    return AgentResponse(
                        handler_type=HandlerType.NEXT,
                        next_handler=handler
                    )
                else:
                    # Se não for um handler válido, usa o handler de conteudo_materia como padrão
                    return AgentResponse(
                        handler_type=HandlerType.NEXT,
                        next_handler="conteudo_materia"
                    )
            
            # Para outros agents, a resposta é a mensagem final
            return AgentResponse(
                handler_type=HandlerType.FINAL,
                message=content
            )
            
        except Exception as e:
            self.logger.error(f"Erro no OpenAIAgent: {str(e)}")
            raise openai.error.OpenAIError(f"Erro ao processar mensagem com OpenAI: {str(e)}") 