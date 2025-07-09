from flet import Page,Control
from typing import Any, Callable, Dict, Optional

from flet.core.ref import Ref

from fasp.atom import Atom
from fasp.selector import Selector


class StateManager:
    """
    Gerenciador de estado global reativo.
    Cada chave representa um atom individual e isolado.
    """

    def __init__(self):
        self._atoms: Dict[str, Atom] = {}
        self._selectors: Dict[str, Selector] = {}

    def atom(self, key: str, default: Optional[Any] = None) -> Atom:
        """
        Retorna um atom associado à chave ou cria se não existir.
        """

        if key in self._selectors:
            raise ValueError(f"Chave \'{key}\' já está registrada como selector")

        if key not in self._atoms:
            self._atoms[key] = Atom(default, key=key) # Passa a chave para o Atom

        return self._atoms[key]

    def add_selector(self, key: str, select_fn: Callable[[Callable[[str], Any]], Any]):
        """
        Cria um atom derivado que se atualiza com base em outros.
        """

        if key in self._atoms:
            raise ValueError(f"Chave \'{key}\' já está registrada como Atom.")

        if key not in self._selectors:
            self._selectors[key] = Selector(select_fn, self.atom)
        return self._selectors[key]

    def get(self, key: str) -> Any:
        """Obtém o valor atual de um atom."""

        if key in self._selectors:
            return self._selectors[key].value

        return self.atom(key).value

    def set(self, key: str, value: Any) -> None:
        """Define o valor de um atom."""
        self._set_atom_value(key, value)

    def _set_atom_value(self, key: str, value: Any) -> None:
        """
        Método interno para definir o valor de um atom.
        """
        self.atom(key)._set_value(value)

    def bind(self, key: str, control: Ref, prop: str = "value", update: bool = True) -> None:
        """
        Liga um controle a um atom reativo, reatualizando automaticamente.
        """

        if key in self._selectors:
            self._selectors[key].bind(control, prop, update)
        else:
            self.atom(key).bind(control, prop, update)

    def bind_dynamic(self, key: str, control: Control | Ref, prop: str = "value", update: bool = True):
        """
        Faz bind em um controle direto ou Ref, atualizando sua propriedade automaticamente.
        """

        if key in self._selectors:
            self._selectors[key].bind_dynamic(control, prop, update)
        else:
            self.atom(key).bind_dynamic(control, prop, update)

    def bind_two_way(self, key: str, control: Ref, prop: str = "value"):
        if key in self._selectors:
            raise ValueError("bind_two_way não é permitido em selectors")

        # Agora, o bind_two_way do Atom chamará StateManager.set
        self.atom(key).bind_two_way(control, prop, self.set)

    def unbind(self, key: str, target: Control | Ref):
        """
        Remove o binding de um controle (ou Ref) do estado.
        """

        atom = self._selectors.get(key) or self._atoms.get(key)

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

        atom = self._selectors[key] if key in self._selectors else self.atom(key)

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
        atom = self._selectors.get(key) or self._atoms.get(key)
        if atom:
            atom.unlisten(callback)

    def has(self, key: str) -> bool:
        """
        Verifica se uma chave existe no estado (ou seja, se foi criada).
        """

        return key in self._atoms or key in self._selectors

    def reset(self, key: str, value: Any = None) -> None:
        """
        Reseta o valor de um atom específico. Agora usa o método interno _set_atom_value.
        """

        if key in self._atoms:
            self._set_atom_value(key, value)
        elif key in self._selectors:
            # Selectors não podem ser resetados diretamente, pois são derivados
            raise ValueError(f"Selector \'{key}\' não pode ser resetado diretamente.")

    def delete(self, key: str):
        self._atoms.pop(key, None)
        self._selectors.pop(key, None)

    def clear(self) -> None:
        """
        Remove todos os atoms e ouvintes associados.
        Ideal para logout ou reinicialização completa da sessão.
        """

        for atom in self._atoms.values():
            atom.clear_listeners()

        for s in self._selectors.values():
            s.clear_listeners()

        self._atoms.clear()
        self._selectors.clear()

    def invalidate(self, key: str):
        """
        Força a recomputação de um selector.
        """

        if key in self._selectors:
            self._selectors[key].recompute()

    def selector(self, key: str):
        """
        Decorador que registra uma função como selector dentro de StateManager.
        O estado deve ser explicitamente instanciado em algum ponto.

        Exemplo:
            @selector("full_name")
            def full_name(get):
                return f"{get(\'first_name\')} {get(\'last_name\')}"
        """

        def decorator(func):
            self.add_selector(key, func)
            return func  # retorna a função decorada

        return decorator


def get_state_manager(page: Page) -> StateManager:
    """
    Retorna uma instância isolada de estado vinculada à página.
    """

    if not hasattr(page, "_state_manager"):
        setattr(page, "_state_manager", StateManager())

    return getattr(page, "_state_manager")
