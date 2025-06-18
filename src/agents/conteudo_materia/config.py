from dataclasses import dataclass

@dataclass
class AgentConfig:
    model: str
    temperature: float
    max_tokens: int

config = AgentConfig(
    model="gpt-4-1106-preview",
    temperature=0.7,
    max_tokens=2000
) 