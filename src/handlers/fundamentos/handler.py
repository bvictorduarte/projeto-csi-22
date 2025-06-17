from typing import List
from src.agents.base_agent import AgentResponse
from src.handlers.base_handler import Handler

class FundamentosHandler(Handler):
    async def handle(self, context: List[str]) -> AgentResponse:
        return await self.agent.process(context) 