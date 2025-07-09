import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    state = fa.get_state_manager(page)

    # Criação dos átomos
    state.atom("email", "")
    state.atom("user", None)
    state.atom("status", "")

    # Refs
    email_input = ft.Ref[ft.TextField]()
    status_text = ft.Ref[ft.Text]()
    user_text = ft.Ref[ft.Text]()

    # Ação de login simples
    async def login_action(get, set_value, _):
        for i in range(10):
            await asyncio.sleep(0.1)
            set_value("status", f"loading... {i}")

        email = get("email")
        if email:
            set_value("user", {"email": email})
            set_value("status", "Logado")
        else:
            set_value("status", "Email não pode ser vazio")

    login = fa.Action(login_action)

    async def on_login_click(e):
        await login.run_async(state)

    def on_reset_click(e):
        # Redefine apenas o email e status
        state.reset("email", "")
        state.reset("status", "Campos limpos")

    def on_logout_click(e):
        state.clear()
        print("[FASP] Todos os átomos, binds e listeners foram removidos. Estado resetado.")


    # UI
    page.add(
        ft.TextField(label="Email", ref=email_input, on_change=lambda e: state.set("email", e.control.value)),
        ft.Row([
            ft.ElevatedButton("Login", on_click=on_login_click),
            ft.ElevatedButton("Reset", on_click=on_reset_click),
            ft.ElevatedButton("Logout", on_click=on_logout_click),
        ]),
        ft.Text(ref=status_text, color="blue"),
        ft.Text(ref=user_text, color="green"),
    )

    # Binds
    state.bind("status", status_text)
    state.bind("user", user_text)


if __name__ == "__main__":
    ft.app(target=main)

