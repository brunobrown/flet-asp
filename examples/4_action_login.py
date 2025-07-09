import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    # Create state manager for this page
    state: fa.StateManager = fa.get_state_manager(page)

    # Declare reactive atoms
    state.atom("email", "")
    state.atom("password", "")
    state.atom("user", None)
    state.atom("loading", False)
    state.atom("error", "")

    # UI control references
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    user_ref = ft.Ref[ft.Text]()
    error_ref = ft.Ref[ft.Text]()
    loading_ref = ft.Ref[ft.ProgressRing]()

    # Define the login action
    async def login_action(get, set_value, args):
        set_value("loading", True)
        set_value("error", "")
        await asyncio.sleep(1.5)  # simulate network delay

        email = get("email")
        password = get("password")

        # Simulated credential check
        if email == "test@test.com" and password == "123":
            set_value("user", {"email": email})
        else:
            set_value("error", "Invalid credentials")
            set_value("user", None)

        set_value("loading", False)

    # Create Action instance
    login = fa.Action(login_action)

    # Handle button click
    async def on_login_click(e):
        await login.run_async(state)

    # Build UI layout
    page.add(
        ft.Column([
            ft.TextField(
                label="Email",
                ref=email_ref,
                on_change=lambda e: state.set("email", e.control.value)
            ),
            ft.TextField(
                label="Password",
                ref=password_ref,
                password=True,
                on_change=lambda e: state.set("password", e.control.value)
            ),
            ft.ElevatedButton("Login", on_click=on_login_click),
            ft.ProgressRing(ref=loading_ref),
            ft.Text(ref=error_ref, color="red"),
            ft.Text(ref=user_ref, color="green")
        ])
    )

    # Bind atoms to UI controls
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref, prop="value")
    state.bind("user", user_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
