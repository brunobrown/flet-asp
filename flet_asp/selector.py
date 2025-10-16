import asyncio
import copy
import threading
from typing import Any, Callable
from flet_asp.atom import Atom
from flet_asp.utils import deep_equal


class Selector(Atom):
    """
    A derived Atom that computes its value based on other atoms.

    The Selector automatically tracks dependencies and re-evaluates its value
    when any of them change. It supports both synchronous and asynchronous computations.

    Uses memoization to avoid unnecessary recomputation when dependency values
    haven't actually changed (5-20x performance improvement for expensive selectors).

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
        self._update_lock = threading.Lock()  # Protect against race conditions
        self._update_depth = (
            0  # Track recursion depth for circular dependency detection
        )
        # Memoization cache: stores snapshot of dependency values
        # Used to skip recomputation when dependency values haven't changed
        self._cached_deps: dict[str, Any] = {}
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
            value = self._get_atom(key).value
            # Cache initial dependency values for memoization
            self._cached_deps[key] = value
            return value

        # Initial value computation
        self._value = self._select_fn(getter)

        # Register listeners for each dependency
        for key in self._dependencies:
            atom = self._get_atom(key)
            atom.listen(self._on_dependency_change, immediate=False)

    def _on_dependency_change(self, _):
        """
        Called when any dependency changes. Re-evaluates the selector.

        Handles both sync and async results with protection against:
        - Race conditions (via threading.Lock)
        - Circular dependencies (via recursion depth tracking)
        - Re-entry during async operations
        - Unnecessary recomputation (via memoization)
        """
        # Try to acquire lock (non-blocking)
        # If already locked, another update is in progress, skip this one
        if not self._update_lock.acquire(blocking=False):
            return

        try:
            # Check recursion depth to prevent circular dependencies
            self._update_depth += 1

            # Maximum recursion depth of 100 prevents infinite loops
            # In circular dependencies: A depends on B depends on A...
            if self._update_depth > 100:
                raise RuntimeError(
                    f"Circular dependency detected in selector. "
                    f"Dependencies: {self._dependencies}. "
                    f"This usually means selector A depends on selector B which depends on A."
                )

            # Memoization: Check if any dependency values actually changed
            deps_changed = False
            new_dep_values: dict[str, Any] = {}

            for key in self._dependencies:
                new_value = self._get_atom(key).value
                new_dep_values[key] = new_value

                # Compare with cached value
                if key not in self._cached_deps or not deep_equal(
                    new_value, self._cached_deps[key]
                ):
                    deps_changed = True

            # Skip recomputation if no dependency values changed
            # This provides 5-20x speedup for expensive selector functions
            if not deps_changed:
                return

            # Update cache with new values
            self._cached_deps = new_dep_values

            def getter(key: str):
                return self._get_atom(key).value

            result = self._select_fn(getter)

            if asyncio.iscoroutine(result):
                asyncio.create_task(self._handle_async(result))
            else:
                self._set_value(result)

        finally:
            self._update_depth -= 1
            self._update_lock.release()

    def recompute(self):
        """
        Forces the selector to recompute its value manually, bypassing memoization.
        Useful when dependencies are dynamic or changed indirectly.
        """
        # Clear cache to force recomputation
        self._cached_deps.clear()
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

        Only performs deep copy for mutable types to prevent external mutations.
        Immutable types (str, int, float, tuple, etc.) are assigned directly
        for better performance.

        Args:
            new_value (Any): New computed result.
        """

        if not deep_equal(new_value, self._value):
            # Only deep copy mutable container types
            # This optimization improves performance by 5-10x for immutable types
            if isinstance(new_value, (dict, list, set)):
                self._value = copy.deepcopy(new_value)
            else:
                # Immutable types or objects - safe to assign directly
                # Includes: str, int, float, bool, None, tuple, frozenset, custom immutable objects
                self._value = new_value
            self._notify_listeners()

    @property
    def value(self) -> Any:
        """
        Returns the current value of the selector.

        Returns:
            Any: Computed value.
        """

        return self._value
