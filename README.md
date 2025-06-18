# Assistente de POO 🎓

Um chatbot especializado em ensinar Programação Orientada a Objetos (POO), desenvolvido com Python e integrado com a API da OpenAI. O sistema utiliza diversos padrões de design para garantir uma arquitetura robusta, extensível e de fácil manutenção.

## 📋 Visão Geral

O assistente é capaz de:
- Responder perguntas sobre fundamentos de POO
- Explicar padrões de design
- Auxiliar com dúvidas específicas da disciplina
- Fornecer exemplos práticos em Python
- Monitorar e registrar interações
- Coletar métricas de uso

## 🏗️ Arquitetura e Padrões de Design

### 1. Singleton Pattern
**Onde**: Implementado na classe `Registry` (`src/registry.py`)
```python
class Registry:
    _instance: Optional['Registry'] = None
    
    def __new__(cls) -> 'Registry':
        if cls._instance is None:
            cls._instance = super(Registry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
```
**Como Funciona**:
1. Quando `Registry()` é chamado pela primeira vez:
   - `__new__` verifica se `_instance` é None
   - Cria uma nova instância e armazena em `_instance`
   - Define `_initialized` como False
2. Nas chamadas subsequentes:
   - `__new__` retorna a instância existente
   - `__init__` verifica `_initialized` e retorna sem reinicializar
3. Isso garante que todos os componentes do sistema usem a mesma configuração e registro de handlers

**Benefícios**:
- Garante uma única instância do registro de handlers e agents
- Centraliza o gerenciamento de dependências
- Evita duplicação de recursos e configurações

### 2. Observer Pattern
**Onde**: Implementado em `src/utils/observer.py`
```python
class MessageSubject:
    def __init__(self):
        self._observers: List[Observer] = []
        
    def notify(self, message: str, role: str, handler_type: str) -> None:
        message_info = {
            "content": message,
            "role": role,
            "handler_type": handler_type,
            "timestamp": datetime.now().isoformat()
        }
        for observer in self._observers:
            observer.update(message_info)

class LoggingObserver(Observer):
    def update(self, message: Dict[str, Any]) -> None:
        self.logger.info(
            f"[{message['role']}] [{message['handler_type']}] {message['content'][:100]}..."
        )

class MetricsObserver(Observer):
    def update(self, message: Dict[str, Any]) -> None:
        self.total_messages += 1
        self.messages_per_handler[message["handler_type"]] += 1
        self.messages_per_role[message["role"]] += 1
```
**Como Funciona**:
1. O `ChatController` mantém uma instância de `MessageSubject`
2. Observadores (Logging e Metrics) se registram no subject
3. Quando uma mensagem é processada:
   - `notify()` é chamado com detalhes da mensagem
   - Cada observador recebe a notificação via `update()`
   - Logging registra a mensagem nos logs
   - Metrics atualiza contadores e estatísticas
4. Tudo isso acontece sem que o fluxo principal precise conhecer os detalhes

**Benefícios**:
- Permite monitoramento em tempo real das interações
- Facilita a coleta de métricas
- Desacopla a lógica de logging e métricas do fluxo principal
- Permite adicionar novos observadores sem modificar o código existente

### 3. Chain of Responsibility
**Onde**: Implementado no fluxo de handlers (`src/handlers/`)
```python
class ChatController:
    async def process_message(self, context: List[str]) -> str:
        current_handler = "router"
        while True:
            handler = self.get_handler(current_handler)
            response = await handler.handle(context)
            if response.handler_type == HandlerType.FINAL:
                return response.message
            current_handler = response.next_handler

class RouterHandler(Handler):
    async def handle(self, context: List[str]) -> AgentResponse:
        response = await self.agent.process(context)
        return AgentResponse(
            handler_type=HandlerType.NEXT,
            next_handler=response.message
        )

class FundamentosHandler(Handler):
    async def handle(self, context: List[str]) -> AgentResponse:
        response = await self.agent.process(context)
        return AgentResponse(
            handler_type=HandlerType.FINAL,
            message=response.message
        )
```
**Como Funciona**:
1. O processo começa sempre com o `RouterHandler`
2. Cada handler decide:
   - Se pode processar a mensagem (FINAL)
   - Ou qual próximo handler deve tentar (NEXT)
3. O fluxo típico é:
   - Router analisa a mensagem e decide o handler apropriado
   - Handler específico processa e retorna resposta final
4. Exemplo de cadeia:
   ```
   Mensagem -> Router -> Fundamentos -> Resposta
   Mensagem -> Router -> DesignPatterns -> Resposta
   ```

**Benefícios**:
- Permite o roteamento dinâmico de mensagens
- Facilita a adição de novos handlers
- Separa responsabilidades de processamento
- Mantém o código organizado e modular

### 4. Factory Method
**Onde**: Implementado no `Registry` para criação de handlers
```python
class Registry:
    def __init__(self):
        self.handler_types: Dict[str, Type[Handler]] = {
            "router": RouterHandler,
            "fundamentos_poo": FundamentosHandler,
            "design_patterns": DesignPatternsHandler
        }
        self.agent_configs: Dict[str, Tuple] = {
            "router": (ROUTER_CONFIG, ROUTER_PROMPT),
            "fundamentos_poo": (FUNDAMENTOS_CONFIG, FUNDAMENTOS_PROMPT)
        }

    def create_handler(self, handler_type: str) -> Handler:
        if handler_type not in self.handler_types:
            raise HandlerNotFoundError(f"Tipo de handler não registrado: {handler_type}")
        config, prompt = self.agent_configs[handler_type]
        agent = OpenAIAgent(config=config, system_prompt=prompt)
        handler_class = self.handler_types[handler_type]
        return handler_class(agent=agent)
```
**Como Funciona**:
1. O Registry mantém mapeamentos de:
   - Tipos de handler para suas classes
   - Tipos de handler para suas configurações
2. Quando `create_handler` é chamado:
   - Verifica se o tipo é válido
   - Obtém a configuração específica
   - Cria um agent com a configuração
   - Instancia o handler com o agent
3. Cada handler é criado com sua própria configuração e prompt

**Benefícios**:
- Encapsula a lógica de criação de handlers
- Permite configuração flexível de diferentes tipos de handlers
- Facilita a manutenção e extensão do sistema

### 5. Strategy Pattern
**Onde**: Implementado na estrutura de agents (`src/agents/base_agent.py`)
```python
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
        return AgentResponse(
            handler_type=HandlerType.FINAL,
            message=response.choices[0].message.content
        )
```
**Como Funciona**:
1. A classe base `Agent` define a interface comum
2. Cada implementação de agent:
   - Herda de `Agent`
   - Implementa seu próprio `process()`
   - Usa sua própria configuração
3. Os handlers trabalham com a interface `Agent`:
   - Não precisam conhecer a implementação específica
   - Podem usar qualquer agent que implemente a interface
4. Exemplo de fluxo:
   ```
   Handler -> Agent.process() -> (OpenAIAgent/CustomAgent/MockAgent) -> Response
   ```

**Benefícios**:
- Permite diferentes implementações de processamento de mensagens
- Facilita a adição de novos tipos de agents
- Mantém o código flexível para futuras integrações
- Permite trocar implementações sem afetar o resto do sistema

## 🔄 Fluxo de Processamento

1. O usuário envia uma mensagem
2. O `RouterHandler` determina o handler apropriado
3. O handler específico processa a mensagem usando seu agent
4. Os observadores registram a interação e coletam métricas
5. A resposta é retornada ao usuário

## 📊 Monitoramento e Métricas

O sistema mantém métricas em tempo real:
- Total de mensagens processadas
- Distribuição de mensagens por handler
- Contagem de interações por tipo de usuário
- Logs detalhados para debugging

## 🛠️ Extensibilidade

O sistema foi projetado para ser facilmente extensível:
1. Novos handlers podem ser adicionados implementando a interface `Handler`
2. Novos agents podem ser criados estendendo a classe `Agent`
3. Novos observadores podem ser adicionados implementando a interface `Observer`
4. Novas métricas podem ser coletadas sem modificar o código existente

## 🔐 Boas Práticas

- Tratamento robusto de erros
- Logging estruturado
- Tipagem forte com Python
- Documentação clara
- Princípios SOLID
- Código assíncrono para melhor performance 