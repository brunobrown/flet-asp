import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    state: fa.StateManager = fa.get_state_manager(page)

    state.set("email", "")
    state.set("password", "")
    state.set("user", None)
    state.set("loading", False)
    state.set("error", "")

    # UI refs
    email_input_ref = ft.Ref[ft.TextField]()
    pass_input_ref = ft.Ref[ft.TextField]()
    error_ref = ft.Ref[ft.Text]()
    email_text_ref = ft.Ref[ft.Text]()
    loading_ref = ft.Ref[ft.ProgressRing]()

    # Ação simulada de login
    async def login_action(get, set_value, _):
        set_value("loading", True)
        set_value("error", "")
        await asyncio.sleep(1)

        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
        else:
            set_value("error", "Login inválido")
            set_value("user", None)

        set_value("loading", False)

    login = fa.Action(login_action)

    async def on_login_click(e):
        await login.run_async(state)

    # Selector que observa apenas o email do usuário
    user_email_selector = fa.Selector(
        state=state,
        select_fn=lambda get: (get("user") or {}).get("email", ""),
    )

    # Atualiza o TEXTO sem bind
    def update_control_without_binding(value):
        email_text_ref.current.value = value
        email_text_ref.current.update()

    # Quando o email do usuário muda, atualiza o texto sem bind
    user_email_selector.listen(
        keys=["user"],
        callback=lambda value: update_control_without_binding(value),
        immediate=False
    )

    # Layout
    page.add(
        ft.TextField(label="Email", ref=email_input_ref, on_change=lambda e: state.set("email", e.control.value)),
        ft.TextField(label="Senha", ref=pass_input_ref, password=True, on_change=lambda e: state.set("password", e.control.value)),
        ft.ElevatedButton("Login", on_click=on_login_click),
        ft.ProgressRing(ref=loading_ref),
        ft.Text(ref=error_ref, color="red"),
        ft.Text(ref=email_text_ref, color="green")  # valor será setado pelo selector
    )

    # Binds
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref)


if __name__ == "__main__":
    ft.app(target=main)
