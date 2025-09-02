import asyncio
import copy
from typing import Any, Callable
from flet_asp.atom import Atom
from flet_asp.utils import deep_equal


class Selector(Atom):
    """
    A derived Atom that computes its value based on other atoms.

    The Selector automatically tracks dependencies and re-evaluates its value
    when any of them change. It supports both synchronous and asynchronous computations.

    Example:
        state.add_selector("user_email", lambda get: get("user")["email"])
    """

    def __init__(
        self,
        select_fn: Callable[[Callable[[str], Any]], Any],
        resolve_atom: Callable[[str], Atom],
    ):
        """
        Initializes the Selector.

        Args:
            select_fn (Callable): A function that receives `get(key)` and returns the derived value.
            resolve_atom (Callable): A function that resolves atom instances by key.
        """

        super().__init__(None)
        self._select_fn = select_fn
        self._get_atom = resolve_atom
        self._is_updating = False
        self._dependencies: set[str] = set()
        self._setup_dependencies()

    def __repr__(self):
        return (
            f"<Selector(dependencies={list(self._dependencies)}, value={self._value})>"
        )

    def _setup_dependencies(self):
        """
        Registers the dependencies of the selector by calling the `select_fn`
        with a special getter that tracks the accessed keys.
        """

        def getter(key: str):
            self._dependencies.add(key)
            return self._get_atom(key).value

        # Initial value computation
        self._value = self._select_fn(getter)

        # Register listeners for each dependency
        for key in self._dependencies:
            atom = self._get_atom(key)
            atom.listen(self._on_dependency_change, immediate=False)

    def _on_dependency_change(self, _):
        """
        Called when any dependency changes. Re-evaluates the selector.
        Handles both sync and async results.
        """

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
        """
        Forces the selector to recompute its value manually.
        Useful when dependencies are dynamic or changed indirectly.
        """

        self._on_dependency_change(None)

    async def _handle_async(self, coro):
        """
        Awaits an async value and sets it after resolution.

        Args:
            coro (Coroutine): Awaitable returned by the selector.
        """
        try:
            result = await coro
            self._set_value(result)
        except Exception as e:
            print(f"[Selector async error]: {e}")

    def _set_value(self, new_value: Any):
        """
        Updates the internal value if it differs from the current one.

        Args:
            new_value (Any): New computed result.
        """

        if not deep_equal(new_value, self._value):
            self._value = copy.deepcopy(new_value)
            self._notify_listeners()

    @property
    def value(self) -> Any:
        """
        Returns the current value of the selector.

        Returns:
            Any: Computed value.
        """

        return self._value
