from typing import Any, Callable
from flet_asp.state import StateManager


class Action:
    """
    Represents an action that can read from and modify the global state.

    Ideal for encapsulating business logic and side effects, such as
    asynchronous requests, validation, or multi-step workflows.

    The action receives `get()` and `set()` functions to interact with the state
    as well as an optional `args` parameter.

    Example:
        async def login(get, set_value, args):
            set_value("loading", True)
            ...
            set_value("user", {"email": get("email")})

        login_action = Action(login)
    """

    def __init__(
        self,
        handler: Callable[[Callable[[str], Any], Callable[[str, Any], None], Any], Any],
    ):
        """
        Initializes the Action.

        Args:
            handler (Callable): A function with signature (get, set, args)
                used to execute the logic.
        """

        self.handler = handler

    def run(self, state: StateManager, args: Any = None):
        """
        Executes the action synchronously.

        Args:
            state (StateManager): The state instance.
            args (Any, optional): Optional arguments passed to the handler.

        Returns:
            Any: The result of the handler execution.
        """

        get = state.get
        set_value = state.set

        return self.handler(get, set_value, args)

    async def run_async(self, state: StateManager, args: Any = None):
        """
        Executes the action asynchronously.

        Should be used when the handler is an async coroutine (e.g., API call).

        Args:
            state (StateManager): The state instance.
            args (Any, optional): Optional arguments passed to the handler.

        Returns:
            Any: Awaited result of the async handler.
        """

        get = state.get
        set_value = state.set

        return await self.handler(get, set_value, args)
