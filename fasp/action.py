from typing import Any, Callable
from fasp.state import StateManager


class Action:
    """
    Representa uma ação que pode ler e modificar o estado global.
    Ideal para lógica de negócio com efeitos colaterais.
    """

    def __init__(self, handler: Callable[[Callable[[str], Any], Callable[[str, Any], None], Any], Any]):
        """
        handler: função com assinatura (get, set, args) → resultado
        """
        
        self.handler = handler

    def run(self, state: StateManager, args: Any = None):
        """
        Executa a ação com acesso ao estado (get/set) e argumentos.
        """

        get = state.get
        set_value = state.set
        return self.handler(get, set_value, args)

    async def run_async(self, state: StateManager, args: Any = None):
        """
        Executa a ação de forma assíncrona (caso a função handler seja async).
        """

        get = state.get
        set_value = state.set
        return await self.handler(get, set_value, args)
