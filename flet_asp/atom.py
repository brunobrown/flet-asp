from flet import Control, Ref
from typing import Any, Callable, List
from flet_asp.utils import deep_equal


class Atom:
    """
    A reactive and observable unit of state.

    Atoms store raw values and notify listeners or UI bindings when updated.
    This class is the core of the Flet-ASP pattern, enabling one-way or two-way reactivity.

    NOTE: To ensure predictability, this class does not expose a public `set()` method.
    Use `StateManager.set(key, value)` to update the atom value.

    Attributes:
        _value (Any): The current state value.
        _listeners (list[Callable]): Functions to call when value changes.
        key (str): Optional identifier for debug purposes.
    """

    def __init__(self, value: Any, key: str = ""):
        """
        Initializes a new Atom.

        Args:
            value (Any): Initial state value.
            key (str, optional): Debug identifier.
        """

        self._value: Any = value
        self._listeners: List[Callable[[Any], None]] = []
        self.key: str = key

    def __repr__(self):
        return f"<Atom(key='{self.key}', value={self._value}, listeners={len(self._listeners)})>"

    @property
    def value(self) -> Any:
        """
        Gets the current value of the atom.

        Returns:
            Any: Current value.
        """

        return self._value

    def _set_value(self, value: Any) -> None:
        """
        Updates the atom value and notifies listeners if it changed.

        NOTE: This should only be called by StateManager.

        Args:
            value (Any): New value.
        """

        if isinstance(value, (dict, list)) or not deep_equal(self._value, value):
            self._value = value
            self._notify_listeners()

    def _notify_listeners(self) -> None:
        """Calls all listeners with the updated value."""

        for callback in self._listeners:
            callback(self._value)

    def listen(self, callback: Callable[[Any], None], immediate: bool = True) -> None:
        """
        Adds a listener that will be called when the value changes.

        Args:
            callback (Callable): The function to call.
            immediate (bool): If True, call immediately with current value.
        """

        if callback not in self._listeners:
            self._listeners.append(callback)
            if immediate:
                callback(self._value)

    def unlisten(self, callback: Callable[[Any], None]):
        """
        Removes a previously registered listener.

        Args:
            callback (Callable): Listener to remove.
        """

        self._listeners = [cb for cb in self._listeners if cb != callback]

    def bind(self, control: Ref, prop: str = "value", update: bool = True):
        """
        Binds the atom to a UI control (Ref).

        Automatically updates the control's property when the value changes.

        Args:
            control (Ref): A Flet Ref to the UI component.
            prop (str): The property to update (e.g., "value").
            update (bool): Whether to call `update()` after setting the property.
        """

        def listener(value):
            if control.current is not None:
                setattr(control.current, prop, value)
                if update:
                    control.current.update()

        # Prevent duplicate bindings
        for existing_listener in self._listeners:
            if getattr(existing_listener, "__ref__", None) is control:
                return

        listener.__ref__ = control
        self._listeners.append(listener)
        listener(self._value)

    def bind_dynamic(
        self, control: Control | Ref, prop: str = "value", update: bool = True
    ):
        """
        Binds the atom to either a control or a Ref dynamically.

        Args:
            control (Control | Ref): Control or Ref instance.
            prop (str): UI property to update.
            update (bool): Call update() after assignment.
        """

        is_ref = hasattr(control, "current")
        target = control.current if is_ref else control

        def listener(value):
            if target is not None:
                setattr(target, prop, value)
                if update:
                    target.update()

        for existing_listener in self._listeners:
            if is_ref:
                if getattr(existing_listener, "__ref__", None) is getattr(
                    target, "ref", None
                ):
                    return
            else:
                if getattr(existing_listener, "__control_id__", None) == id(target):
                    return

        if is_ref:
            listener.__ref__ = target
        else:
            listener.__control_id__ = id(target)

        self._listeners.append(listener)
        listener(self._value)

    def unbind(self, target: Control | Ref):
        """
        Removes the listener bound to a specific control or Ref.

        Args:
            target (Control | Ref): UI component or Ref to unbind.
        """

        if isinstance(target, Ref):
            self._listeners = [
                listener
                for listener in self._listeners
                if getattr(listener, "__ref__", None) is not target
            ]
        elif isinstance(target, Control):
            self._listeners = [
                listener
                for listener in self._listeners
                if getattr(listener, "__control_id__", None) != id(target)
            ]

    def bind_two_way(
        self,
        control: Ref,
        prop: str = "value",
        update: bool = True,
        on_input_change: Callable = None,
    ):
        """
        Creates a two-way binding between the atom and an input control.

        This allows updating the UI when the state changes and vice versa.

        Args:
            control (Ref): Ref of the UI input.
            prop (str): Property to sync.
            update (bool): Whether to update the control visually.
            on_input_change (Callable, optional): Custom change handler.
        """

        def listener(value):
            setattr(control.current, prop, value)
            if update:
                control.current.update()

        listener.__control_id__ = id(control)
        self.listen(listener)

        # Input → state
        def on_change(e):
            new_value = getattr(control.current, prop)
            self._set_value(new_value)

        control.current.on_change = on_input_change or on_change

    def clear_listeners(self) -> None:
        """
        Removes all listeners (UI or logic) from this atom.
        """

        self._listeners.clear()

    def has_listeners(self) -> bool:
        """
        Checks whether the atom has any active listeners.

        Returns:
            bool: True if listeners exist.
        """

        return len(self._listeners) > 0
