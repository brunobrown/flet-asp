from flet import Control, Ref
from typing import Any, Callable, List
from fasp.utils import deep_equal


class Atom:
    """
    Representa uma unidade de estado reativo.
    Pode ter múltiplos ouvintes, incluindo UI (bind) ou lógica (listen).
    """

    def __init__(self, value: Any):
        self._value: Any = value
        self._listeners: List[Callable[[Any], None]] = []

    def __repr__(self):
        return f"<Atom(value={self._value}, listeners={len(self._listeners)})>"

    @property
    def value(self) -> Any:
        """Retorna o valor atual do atom."""
        return self._value

    def set(self, value: Any) -> None:
        """Atualiza o valor e notifica os ouvintes se houver mudança."""

        if not deep_equal(self._value, value):
            self._value = value
            self._notify_listeners()

    def _notify_listeners(self) -> None:
        for callback in self._listeners:
            callback(self._value)

    def listen(self, callback: Callable[[Any], None], immediate: bool = True) -> None:
        """
        Adiciona um ouvinte que será chamado sempre que o valor mudar.
        Se `immediate` for True, o ouvinte será chamado imediatamente com o valor atual.
        """

        if callback not in self._listeners:
            self._listeners.append(callback)
            if immediate:
                callback(self._value)

    def unlisten(self, callback: Callable[[Any], None]):
        self._listeners = [cb for cb in self._listeners if cb != callback]

    def bind(self, control: Ref, prop: str = "value", update: bool = True):
        """
        Faz bind em um Ref, atualizando sua propriedade automaticamente.

        Observe: O controle deve estar na página.
        """

        def listener(value):
            if control.current is not None:
                setattr(control.current, prop, value)

                if update:
                    control.current.update()

        # Verifica se essa Ref já está registrada
        for existing_listener in self._listeners:
            if getattr(existing_listener, "__ref__", None) is control:
                return  # Já está vinculado

        # Marca esse listener com a Ref diretamente
        listener.__ref__ = control
        self._listeners.append(listener)
        listener(self._value)

    def bind_dynamic(self, control: Control | Ref, prop: str = "value", update: bool = True):
        """
        Faz bind direto em controle ou Ref e atualiza sua propriedade automaticamente.

        Observe: O controle deve ser adicionado à página primeiro.
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
                # Verifica se essa Ref já está registrada
                if getattr(existing_listener, "__ref__", None) is getattr(target, 'ref', None):
                    return  # Já está vinculado
            else:
                # Verifica se esse Control já está registrado
                if getattr(existing_listener, "__control_id__", None) == id(target):
                    return # Já está vinculado

        if is_ref:
            # Marca esse listener com a Ref
            listener.__ref__ = target.current.ref
        else:
            # Marca esse listener com o control
            listener.__control_id__ = id(target)

        self._listeners.append(listener)
        listener(self._value)

    def unbind(self, target: Control | Ref):
        """
        Remove o listener associado a uma Ref ou Control.
        """

        if isinstance(target, Ref):
            self._listeners = [
                listener for listener in self._listeners
                if getattr(listener, "__ref__", None) is not target
            ]

        elif isinstance(target, Control):
            self._listeners = [
                listener for listener in self._listeners
                if getattr(listener, "__control_id__", None) != id(target)
            ]

    def bind_two_way(self, control: Ref, prop: str = "value", update: bool = True):
        """
        Sincroniza o estado com o controle e vice-versa.
        Reage à mudança no controle e atualiza o estado, e vice-versa.
        """

        def listener(value):
            setattr(control.current, prop, value)

            if update:
                control.current.update()

        listener.__control_id__ = id(control)

        # Reação: estado → UI
        self.listen(listener)

        # Reação: UI → estado
        def on_change(e):
            self.set(getattr(control.current, prop))
        control.current.on_change = on_change

    def clear_listeners(self) -> None:
        """Remove todos os ouvintes registrados para este atom."""
        self._listeners.clear()

    def has_listeners(self) -> bool:
        """Retorna True se este atom tiver ouvintes ativos."""
        return len(self._listeners) > 0
