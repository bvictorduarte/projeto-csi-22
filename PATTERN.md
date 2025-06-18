# Padrões de Design no POO Chat 🎨

Este documento detalha os principais padrões de design utilizados no projeto POO Chat, explicando como cada padrão é implementado e seu propósito no sistema.

## Strategy Pattern 🎯

*O que é?*  
O Strategy é um padrão comportamental que permite definir uma família de algoritmos, encapsular cada um deles e torná-los intercambiáveis. Permite que o algoritmo varie independentemente dos clientes que o utilizam.

*Como é usado no projeto?*  
No POO Chat, o Strategy é implementado na estrutura de Agents para permitir diferentes implementações de processamento de mensagens. A classe base Agent define a interface comum, enquanto classes concretas como OpenAIAgent implementam comportamentos específicos.

*Código Relevante:*
python
# src/agents/base_agent.py
class Agent(ABC):
    def __init__(self, config: AgentConfig, system_prompt: str):
        self.config = config
        self.system_prompt = system_prompt

    @abstractmethod
    async def process(self, context: list[str]) -> AgentResponse:
        pass

class OpenAIAgent(Agent):
    async def process(self, context: list[str]) -> AgentResponse:
        response = await openai.ChatCompletion.acreate(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": context[-1]}
            ]
        )
        return AgentResponse(...)


*Benefícios no projeto:*
- Permite diferentes implementações de processamento de mensagens
- Facilita a adição de novos tipos de agents (ex: Anthropic, Hugging Face)
- Mantém o código flexível para futuras integrações
- Isola o algoritmo de processamento de mensagens do resto do sistema

## Chain of Responsibility Pattern ⛓️

*O que é?*  
O Chain of Responsibility é um padrão comportamental que permite passar solicitações ao longo de uma cadeia de handlers. Cada handler decide se processa a solicitação ou a passa adiante na cadeia.

*Como é usado no projeto?*  
O POO Chat implementa este padrão no fluxo de processamento de mensagens. O RouterHandler inicia a cadeia e decide qual handler específico deve processar a mensagem. Cada handler pode decidir processar a mensagem (FINAL) ou passá-la adiante (NEXT).

*Código Relevante:*
python
# src/controllers/chat_controller.py
async def process_message(self, context: List[str]) -> str:
    try:
        current_handler = "router"
        while True:
            handler = self.get_handler(current_handler)
            response = await handler.handle(context)
            
            if response.handler_type == HandlerType.FINAL:
                return response.message
            
            current_handler = response.next_handler

# src/handlers/base_handler.py
class Handler(ABC):
    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    async def handle(self, context: List[str]) -> AgentResponse:
        pass


*Benefícios no projeto:*
- Permite roteamento dinâmico de mensagens
- Desacopla o processamento em diferentes handlers
- Facilita a adição de novos handlers
- Mantém o fluxo de processamento flexível e extensível

## Singleton Pattern 🔒

*O que é?*  
O Singleton é um padrão criacional que garante que uma classe tenha apenas uma instância e fornece um ponto global de acesso a ela.

*Como é usado no projeto?*  
O padrão Singleton é implementado na classe Registry, que atua como um registro central para handlers e agents. Isso garante que todo o sistema use a mesma configuração e registro de handlers.

*Código Relevante:*
python
# src/registry.py
class Registry:
    _instance: Optional['Registry'] = None
    
    def __new__(cls) -> 'Registry':
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.handler_types: Dict[str, Type[Handler]] = {
            "router": RouterHandler,
            "conteudo_materia": ConteudoMateriaHandler,
            "disciplina_info": DisciplinaInfoHandler
        }
        
        self._initialized = True


*Benefícios no projeto:*
- Garante uma única instância do registro de handlers e agents
- Centraliza o gerenciamento de dependências
- Evita duplicação de recursos e configurações
- Fornece um ponto global de acesso controlado

## Interação entre os Padrões 🔄

Os três padrões trabalham em conjunto no POO Chat:

1. O *Singleton* (Registry) mantém o registro central de handlers e suas configurações

2. O *Chain of Responsibility* usa o Registry para obter os handlers necessários e estabelece o fluxo de processamento

3. O *Strategy* é usado pelos handlers para processar mensagens de diferentes maneiras através dos agents

Esta combinação cria uma arquitetura:
- Flexível: Fácil de estender com novos handlers e agents
- Modular: Componentes bem definidos e desacoplados
- Manutenível: Responsabilidades claramente separadas
- Escalável: Preparada para crescer com novas funcionalidades