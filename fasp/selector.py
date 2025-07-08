from typing import Any, Callable
from fasp.state import StateManager


class Selector:
    """
    Permite derivar valores baseados no estado atual.
    Pode ser usado em UI ou lógica, como um Computed leve e imediato.
    """

    def __init__(self, state: StateManager, select_fn: Callable[[Callable[[str], Any]], Any]):
        self._state = state
        self._select_fn = select_fn

    @property
    def value(self) -> Any:
        return self._select_fn(self._state.get)

    def listen(self, keys: list[str], callback: Callable[[Any], None], immediate: bool = True):
        """
        Escuta mudanças em múltiplas chaves que afetam esse selector.

        Exemplo:
            selector.listen(["user", "profile"], lambda v: print(v))
        """

        for key in keys:
            self._state.listen(key, lambda _: callback(self.value), immediate=immediate)
