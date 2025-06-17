from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import openai
import os

class HandlerType(Enum):
    NEXT = "next"
    FINAL = "final"

@dataclass
class AgentResponse:
    handler_type: HandlerType
    next_handler: Optional[str] = None
    message: Optional[str] = None

class AgentConfig:
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

class Agent(ABC):
    def __init__(self, config: AgentConfig, system_prompt: str):
        self.config = config
        self.system_prompt = system_prompt

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
        """
        response = openai.ChatCompletion.create(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": context[-1]}  # Última mensagem do contexto
            ]
        )

        content = response.choices[0].message.content.strip()

        # Se for o router, a resposta é o próximo handler
        if "fundamentos_poo" in self.system_prompt.lower():
            return AgentResponse(
                handler_type=HandlerType.NEXT,
                next_handler=content
            )
        
        # Para outros agents, a resposta é a mensagem final
        return AgentResponse(
            handler_type=HandlerType.FINAL,
            message=content
        ) 