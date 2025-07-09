import asyncio
import copy
from typing import Any, Callable
from fasp.atom import Atom
from fasp.utils import deep_equal


class Selector(Atom):
    """
    Um Atom derivado que calcula seu valor com base em outros atoms.
    Atualiza automaticamente sempre que qualquer dependência mudar.
    Pode lidar com computações síncronas e assíncronas.
    """

    def __init__(self, select_fn: Callable[[Callable[[str], Any]], Any], resolve_atom: Callable[[str], Atom]):
        super().__init__(None)
        self._select_fn = select_fn
        self._get_atom = resolve_atom
        self._is_updating = False
        self._dependencies: set[str] = set()
        self._setup_dependencies()

    def __repr__(self):
        return f"<Selector(dependencies={list(self._dependencies)}, value={self._value})>"

    def _setup_dependencies(self):
        def getter(key: str):
            self._dependencies.add(key)
            return self._get_atom(key).value

        self._value = self._select_fn(getter)  # valor inicial

        for key in self._dependencies:
            atom = self._get_atom(key)
            atom.listen(self._on_dependency_change, immediate=False)

    def _on_dependency_change(self, _):
        if self._is_updating:
            return

        self._is_updating = True

        def getter(key: str):
            return self._get_atom(key).value

        result = self._select_fn(getter)

        if asyncio.iscoroutine(result):
            asyncio.create_task(self._handle_async(result))
        else:
            self._set_value(result)

        self._is_updating = False

    def recompute(self):
        self._on_dependency_change(None)

    async def _handle_async(self, coro):
        try:
            result = await coro
            self._set_value(result)
        except Exception as e:
            print(f"[Selector async error]: {e}")

    def _set_value(self, new_value: Any):
        if not deep_equal(new_value, self._value):
            self._value = copy.deepcopy(new_value)
            self._notify_listeners()

    @property
    def value(self) -> Any:
        return self._value


