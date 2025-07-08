import inspect
from flet import Page,Control
from typing import Any, Callable, Dict, Optional

from flet.core.ref import Ref

from fasp.atom import Atom
from fasp.computed import Computed


class StateManager:
    """
    Gerenciador de estado global reativo, inspirado no padrão Riverpod.
    Cada chave representa um atom individual e isolado.
    """

    def __init__(self):
        self._atoms: Dict[str, Atom] = {}
        self._computed: Dict[str, Computed] = {}

    def atom(self, key: str, default: Optional[Any] = None) -> Atom:
        """
        Retorna um atom associado à chave, criando se não existir.
        """

        if key in self._computed:
            raise ValueError(f"Chave '{key}' já está registrada como computed")

        if key not in self._atoms:
            self._atoms[key] = Atom(default)

        return self._atoms[key]

    def add_computed(self, key: str, compute_fn: Callable[[Callable[[str], Any]], Any]):
        """
        Cria um atom derivado que se atualiza com base em outros.
        """

        if key in self._computed:
            raise ValueError(f"Chave '{key}' já está registrada como Atom.")

        if key not in self._computed:
            self._computed[key] = Computed(compute_fn, self.atom)
        return self._computed[key]

    def get(self, key: str) -> Any:
        """Obtém o valor atual de um atom."""

        if key in self._computed:
            return self._computed[key].value

        return self.atom(key).value

    def set(self, key: str, value: Any) -> None:
        """Define o valor de um atom."""

        self.atom(key).set(value)

    def bind(self, key: str, control: Ref, prop: str = "value", update: bool = True) -> None:
        """
        Liga um controle a um atom reativo, reatualizando automaticamente.
        """

        if key in self._computed:
            self._computed[key].bind(control, prop, update)
        else:
            self.atom(key).bind(control, prop, update)

    def bind_dynamic(self, key: str, control: Control | Ref, prop: str = "value", update: bool = True):
        """
        Faz bind em um controle direto ou Ref, atualizando sua propriedade automaticamente.
        """

        if key in self._computed:
            self._computed[key].bind_dynamic(control, prop, update)
        else:
            self.atom(key).bind_dynamic(control, prop, update)

    def bind_two_way(self, key: str, control: Ref, prop: str = "value"):
        if key in self._computed:
            raise ValueError("bind_two_way não é permitido em computed")

        self.atom(key).bind_two_way(control, prop)

    def unbind(self, key: str, target: Control | Ref):
        """
        Remove o binding de um controle (ou Ref) do estado.
        """

        atom = self._computed.get(key) or self._atoms.get(key)

        if not atom:
            return

        if isinstance(target, Ref):
            atom.unbind(target)
        elif isinstance(target, Control) and hasattr(target, "ref"):
            atom.unbind(target.ref)

    def listen(self, key: str, callback: Callable[[Any], None], immediate: bool = True) -> None:
        """
        Adiciona um ouvinte a um atom, útil para lógica fora da UI, evitando duplicatas.
        """

        atom = self._computed[key] if key in self._computed else self.atom(key)

        # Verifica se já existe callback registrado (comparando pelo ID)
        if any(cb == callback for cb in atom._listeners):
            return  # Já registrado, evita duplicata

        atom.listen(callback, immediate)

    def listen_multiple(self, keys_callbacks: dict[str, Callable[[Any], None]]):
        """
        Registra múltiplos ouvintes no estado de forma concisa.

        Example:
            listen_to_keys(state, {
                "user_name": on_user_change,
                "theme_mode": on_theme_change,
            })
        """

        for key, callback in keys_callbacks.items():
            self.listen(key, callback)

    def unlisten(self, key: str, callback: Callable[[Any], None]):
        atom = self._computed.get(key) or self._atoms.get(key)
        if atom:
            atom.unlisten(callback)

    def has(self, key: str) -> bool:
        """
        Verifica se uma chave existe no estado (ou seja, se foi criada).
        """

        return key in self._atoms

    def reset(self, key: str, value: Any = None) -> None:
        """Reseta o valor de um atom específico."""

        if key in self._atoms:
            self._atoms[key].set(value)

    def delete(self, key: str):
        self._atoms.pop(key, None)
        self._computed.pop(key, None)

    def clear(self) -> None:
        """
        Remove todos os atoms e ouvintes associados.
        Ideal para logout ou reinicialização completa da sessão.
        """

        for atom in self._atoms.values():
            atom.clear_listeners()

        for c in self._computed.values():
            c.clear_listeners()

        self._atoms.clear()

    def invalidate(self, key: str):
        """
        Força a recomputação de um computed_atom.
        """

        if key in self._computed:
            self._computed[key].recompute()

    def computed(self, key: str):
        """
        Decorador que registra uma função como computed dentro de StateManager.
        O estado deve ser explicitamente instanciado em algum ponto.

        Exemplo:
            @computed("full_name")
            def full_name(get):
                return f"{get('first_name')} {get('last_name')}"
        """

        def decorator(func):
            self.add_computed(key, func)
            return func  # retorna a função decorada

        return decorator


def get_state_manager(page: Page) -> StateManager:
    """
    Retorna uma instância isolada de estado vinculada à página.
    """

    if not hasattr(page, "_state_manager"):
        setattr(page, "_state_manager", StateManager())

    return getattr(page, "_state_manager")
