import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    state = fa.get_state_manager(page)

    state.set("email", "")
    state.set("password", "")
    state.set("user", None)

    # Refs
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    welcome_ref = ft.Ref[ft.Text]()

    # Simula login
    async def login_action(get, set_value, _):
        for i in range(10):
            await asyncio.sleep(0.1)
            welcome_ref.current.value = f"Autenticando... {i}"
            welcome_ref.current.update()

        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
        else:
            set_value("user", None)

    login = fa.Action(login_action)

    # Clique do botão
    async def on_login_click(e):
        await login.run_async(state)

    # Lógica reativa (sem bind)
    def on_user_change(user_data):
        if user_data:
            welcome_ref.current.value = f"Bem-vindo, {user_data['email']}!"
        else:
            welcome_ref.current.value = "Usuário não autenticado."
        welcome_ref.current.update()

    # UI
    page.add(
        ft.TextField(label="Email", ref=email_ref, on_change=lambda e: state.set("email", e.control.value)),
        ft.TextField(label="Senha", ref=password_ref, password=True, on_change=lambda e: state.set("password", e.control.value)),
        ft.ElevatedButton("Entrar", on_click=on_login_click),
        ft.Text(ref=welcome_ref),
    )

    # Observa mudanças em "user"
    state.listen("user", on_user_change)


if __name__ == "__main__":
    ft.app(target=main)
