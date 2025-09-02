# e:/.../flet-asp/tests/test_state.py

import pytest
from flet_asp.state import StateManager


def test_atom_creation_and_retrieval():
    """
    Tests if an atom can be created and its value retrieved correctly.
    """
    manager = StateManager()

    # Cria um novo átomo com um valor padrão
    counter_atom = manager.atom("counter", default=0)

    # Verifica se o valor inicial está correto
    assert manager.get("counter") == 0
    assert counter_atom.value == 0


def test_atom_update():
    """
    Tests if an atom's value can be updated using the set method.
    """
    manager = StateManager()
    manager.atom("user", default="Guest")

    # Atualiza o valor do átomo
    manager.set("user", "Gemini")

    # Verifica se o valor foi atualizado
    assert manager.get("user") == "Gemini"


def test_creating_atom_with_selector_key_raises_error():
    """
    Tests that creating an atom with a key already used by a selector raises a ValueError.
    """
    manager = StateManager()
    manager.add_selector("my_selector", lambda get: "hello")

    with pytest.raises(
        ValueError, match="Key 'my_selector' is already registered as a Selector."
    ):
        manager.atom("my_selector")
