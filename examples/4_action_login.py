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

    # Campo de entrada
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    user_ref = ft.Ref[ft.Text]()
    error_ref = ft.Ref[ft.Text]()
    loading_ref = ft.Ref[ft.ProgressRing]()

    # Definição da ação
    async def login_action(get, set_value, args):
        set_value("loading", True)
        set_value("error", "")
        await asyncio.sleep(1.5)  # simula delay

        email = get("email")
        password = get("password")

        if email == "test@test.com" and password == "123":
            set_value("user", {"email": email})
        else:
            set_value("error", "Credenciais inválidas")
            set_value("user", None)

        set_value("loading", False)

    login = fa.Action(login_action)

    # Botão de login
    async def on_login_click(e):
        await login.run_async(state)

    # Layout
    page.add(
        ft.Column([
            ft.TextField(label="Email", ref=email_ref, on_change=lambda e: state.set("email", e.control.value)),
            ft.TextField(label="Senha", ref=password_ref, password=True, on_change=lambda e: state.set("password", e.control.value)),
            ft.ElevatedButton("Entrar", on_click=on_login_click),
            ft.ProgressRing(ref=loading_ref),
            ft.Text(ref=error_ref, color="red"),
            ft.Text(ref=user_ref, color="green")
        ])
    )

    # Binds
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref, prop="value")
    state.bind("user", user_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
