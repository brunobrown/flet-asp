import pytest
from flet_asp.state import StateManager, get_state_manager


# Classe simples para simular ft.Page sem dependências externas
# pytest tests/test_state_alias.py -v


class MockPage:
    """Mock simples para ft.Page que permite setattr/getattr"""

    pass


class TestStateAlias:
    """
    Testa se o alias 'state' funciona corretamente como alternativa ao '_state_manager'.
    """

    def test_state_alias_exists_after_get_state_manager(self):
        """
        Testa se o alias 'state' é criado após chamar get_state_manager.
        """
        mock_page = MockPage()

        # Chama a função que deve criar o alias
        manager = get_state_manager(mock_page)

        # Verifica se tanto _state_manager quanto state existem
        assert manager is not None
        assert hasattr(mock_page, "_state_manager")
        assert hasattr(mock_page, "state")

    def test_state_and_state_manager_are_same_instance(self):
        """
        Testa se 'state' e '_state_manager' apontam para a mesma instância.
        """
        mock_page = MockPage()

        # Chama a função que cria o state manager
        get_state_manager(mock_page)

        # Verifica se são a mesma instância
        assert mock_page.state is mock_page._state_manager
        assert id(mock_page.state) == id(mock_page._state_manager)

    def test_state_alias_methods_work_correctly(self):
        """
        Testa se todos os métodos funcionam corretamente através do alias 'state'.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Testa atom() via alias
        counter_atom = mock_page.state.atom("counter", default=10)
        assert counter_atom.value == 10

        # Testa get() via alias
        assert mock_page.state.get("counter") == 10

        # Testa set() via alias
        mock_page.state.set("counter", 25)
        assert mock_page.state.get("counter") == 25

    def test_backward_compatibility_maintained(self):
        """
        Testa se código existente usando '_state_manager' continua funcionando.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Usa a forma tradicional
        mock_page._state_manager.atom("user", default="guest")
        mock_page._state_manager.set("user", "admin")

        # Verifica se funciona e se o alias também vê a mudança
        assert mock_page._state_manager.get("user") == "admin"
        assert mock_page.state.get("user") == "admin"

    def test_both_interfaces_modify_same_state(self):
        """
        Testa se mudanças feitas via 'state' são visíveis via '_state_manager' e vice-versa.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Cria átomo via state alias
        mock_page.state.atom("theme", default="light")

        # Modifica via _state_manager
        mock_page._state_manager.set("theme", "dark")

        # Verifica via state alias
        assert mock_page.state.get("theme") == "dark"

        # Modifica via state alias
        mock_page.state.set("theme", "auto")

        # Verifica via _state_manager
        assert mock_page._state_manager.get("theme") == "auto"

    def test_complex_operations_work_with_alias(self):
        """
        Testa operações mais complexas como selectors e listeners via alias.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Cria átomos
        mock_page.state.atom("first_name", default="João")
        mock_page.state.atom("last_name", default="Silva")

        # Cria selector via alias
        @mock_page.state.selector("full_name")
        def full_name(get):
            return f"{get('first_name')} {get('last_name')}"

        # Testa se o selector funciona
        assert mock_page.state.get("full_name") == "João Silva"

        # Testa listener via alias
        callback_called = []

        def on_name_change(value):
            callback_called.append(value)

        mock_page.state.listen("first_name", on_name_change, immediate=False)
        mock_page.state.set("first_name", "Pedro")

        assert callback_called == ["Pedro"]

    def test_get_state_manager_called_multiple_times(self):
        """
        Testa se chamar get_state_manager múltiplas vezes não quebra o alias.
        """
        mock_page = MockPage()

        # Primeira chamada
        manager1 = get_state_manager(mock_page)
        first_state = mock_page.state

        # Segunda chamada
        manager2 = get_state_manager(mock_page)
        second_state = mock_page.state

        # Devem ser as mesmas instâncias
        assert manager1 is manager2
        assert first_state is second_state
        assert mock_page.state is mock_page._state_manager

    def test_alias_preserves_all_state_manager_methods(self):
        """
        Testa se o alias preserva todos os métodos importantes do StateManager.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Lista de métodos que devem estar disponíveis via alias
        expected_methods = [
            "atom",
            "get",
            "set",
            "has",
            "reset",
            "delete",
            "clear",
            "listen",
            "unlisten",
            "bind",
            "unbind",
            "add_selector",
            "selector",
            "invalidate",
            "listen_multiple",
            "bind_dynamic",
            "bind_two_way",
        ]

        for method_name in expected_methods:
            assert hasattr(mock_page.state, method_name)
            assert callable(getattr(mock_page.state, method_name))

    def test_error_handling_works_with_alias(self):
        """
        Testa se o tratamento de erros funciona corretamente via alias.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Cria um selector
        mock_page.state.add_selector("test_selector", lambda get: "computed")

        # Tenta criar átomo com mesmo nome - deve dar erro
        with pytest.raises(
            ValueError, match="Key 'test_selector' is already registered as a Selector"
        ):
            mock_page.state.atom("test_selector")


# Testes de integração mais simples
class TestStateAliasIntegration:
    """
    Testa cenários mais realistas de uso do alias.
    """

    def test_navigation_example_with_alias(self):
        """
        Simula o caso de uso mencionado na issue (navegação SPA).
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Simula configuração de navegação
        mock_page.state.atom("current_page", default="/home")
        mock_page.state.atom("navigation_stack", default=[])

        # Simula action de navegação
        def go_to_page(new_page):
            current = mock_page.state.get("current_page")
            stack = mock_page.state.get("navigation_stack")

            # Adiciona página atual ao stack
            mock_page.state.set("navigation_stack", stack + [current])
            mock_page.state.set("current_page", new_page)

        def go_back():
            stack = mock_page.state.get("navigation_stack")
            if stack:
                previous_page = stack.pop()
                mock_page.state.set("navigation_stack", stack)
                mock_page.state.set("current_page", previous_page)

        # Testa navegação
        go_to_page("/grid/clientes")
        assert mock_page.state.get("current_page") == "/grid/clientes"
        assert mock_page.state.get("navigation_stack") == ["/home"]

        go_to_page("/grid/clientes/form")
        assert mock_page.state.get("current_page") == "/grid/clientes/form"
        assert mock_page.state.get("navigation_stack") == ["/home", "/grid/clientes"]

        # Testa voltar
        go_back()
        assert mock_page.state.get("current_page") == "/grid/clientes"
        assert mock_page.state.get("navigation_stack") == ["/home"]

    def test_multiple_pages_dont_interfere(self):
        """
        Testa se múltiplas páginas têm StateManagers independentes.
        """
        page1 = MockPage()
        page2 = MockPage()

        # Cria state managers para cada página
        manager1 = get_state_manager(page1)
        manager2 = get_state_manager(page2)

        # Devem ser instâncias diferentes
        assert manager1 is not manager2
        assert page1.state is not page2.state

        # Configurações independentes
        page1.state.atom("theme", default="dark")
        page2.state.atom("theme", default="light")

        assert page1.state.get("theme") == "dark"
        assert page2.state.get("theme") == "light"

        # Mudança em uma não afeta a outra
        page1.state.set("theme", "auto")
        assert page1.state.get("theme") == "auto"
        assert page2.state.get("theme") == "light"  # Não mudou

    def test_real_world_form_state_management(self):
        """
        Simula um caso de uso real: gerenciamento de estado de formulário.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Estado do formulário
        mock_page.state.atom("form_data", default={"name": "", "email": "", "age": 0})
        mock_page.state.atom("form_errors", default={})
        mock_page.state.atom("form_loading", default=False)

        # Selector para validação
        @mock_page.state.selector("form_is_valid")
        def form_is_valid(get):
            data = get("form_data")
            return len(data["name"]) > 0 and "@" in data["email"] and data["age"] > 0

        # Estado inicial
        assert not mock_page.state.get("form_is_valid")

        # Preenche formulário
        mock_page.state.set(
            "form_data", {"name": "João Silva", "email": "joao@email.com", "age": 30}
        )

        # Agora deve ser válido
        assert mock_page.state.get("form_is_valid")

        # Testa estado de loading
        mock_page.state.set("form_loading", True)
        assert mock_page.state.get("form_loading")


# Testes específicos para edge cases
class TestStateAliasEdgeCases:
    """
    Testa casos especiais e edge cases.
    """

    def test_page_already_has_state_attribute(self):
        """
        Testa o que acontece se a página já tiver um atributo 'state'.
        """
        mock_page = MockPage()
        # Simula página que já tem 'state'
        mock_page.state = "existing_value"

        # Chama get_state_manager
        get_state_manager(mock_page)

        # O alias deve sobrescrever o valor existente
        assert mock_page.state is not "existing_value"  # noqa
        assert mock_page.state is mock_page._state_manager
        assert isinstance(mock_page.state, StateManager)

    def test_page_methods_work_after_get_state_manager(self):
        """
        Testa se os métodos da página continuam funcionando após adicionar o alias.
        """

        class PageWithMethods(MockPage):
            def custom_method(self):
                return "page_method_result"

        mock_page = PageWithMethods()
        get_state_manager(mock_page)

        # Método da página deve continuar funcionando
        assert mock_page.custom_method() == "page_method_result"

        # Alias state também deve funcionar
        assert hasattr(mock_page, "state")
        assert isinstance(mock_page.state, StateManager)

    def test_state_manager_functionality_not_affected(self):
        """
        Testa se toda a funcionalidade do StateManager permanece intacta.
        """
        mock_page = MockPage()
        get_state_manager(mock_page)

        # Testa funcionalidades avançadas
        mock_page.state.atom("counter", default=0)

        # Listen com callback
        results = []

        def callback(value):
            results.append(value)

        mock_page.state.listen("counter", callback, immediate=True)
        assert results == [0]  # Immediate=True deve chamar com valor atual

        # Múltiplas mudanças
        mock_page.state.set("counter", 5)
        mock_page.state.set("counter", 10)
        assert results == [0, 5, 10]

        # Reset
        mock_page.state.reset("counter", 0)
        assert mock_page.state.get("counter") == 0
        assert results == [0, 5, 10, 0]
