import asyncio
import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example shows how to manage session cleanup in Flet-ASP using two key methods:
        * reset(key, value) → updates specific atoms without affecting others
        * clear() → removes all atoms, selectors, listeners and bindings from the state

    This is useful for scenarios like:
        * Resetting input fields or UI messages
        * Logging the user out
        * Restarting the session completely
    """

    # Initialize the Flet-ASP state manager for this page
    state = fa.get_state_manager(page)

    # Declare reactive atoms
    state.atom("email", "")
    state.atom("user", None)
    state.atom("status", "")

    # UI control references
    email_input = ft.Ref[ft.TextField]()
    status_text = ft.Ref[ft.Text]()
    user_text = ft.Ref[ft.Text]()

    # Async login action with simulated delay
    async def login_action(get, set_value, _):
        # Simulate loading
        for i in range(10):
            await asyncio.sleep(0.1)
            set_value("status", f"Loading... {i}")

        # Basic login logic
        email = get("email")
        if email:
            set_value("user", {"email": email})
            set_value("status", "Logged in")
        else:
            set_value("status", "Email cannot be empty")

    # Create the action
    login = fa.Action(login_action)

    # Trigger login
    async def on_login_click(e):
        await login.run_async(state)

    # Reset specific atoms
    def on_reset_click(e):
        state.reset("email", "")
        state.reset("status", "Fields cleared")

    # Clear entire state (atoms, listeners, binds)
    def on_logout_click(e):
        state.clear()
        print("[Flet-ASP] All atoms, bindings, and listeners removed. State cleared.")

    # Build the UI
    page.add(
        ft.TextField(
            label="Email",
            ref=email_input,
            on_change=lambda e: state.set("email", e.control.value)
        ),
        ft.Row([
            ft.ElevatedButton("Login", on_click=on_login_click),
            ft.ElevatedButton("Reset", on_click=on_reset_click),
            ft.ElevatedButton("Logout", on_click=on_logout_click),
        ]),
        ft.Text(ref=status_text, color="blue"),
        ft.Text(ref=user_text, color="green"),
    )

    # Bind atoms to display elements
    state.bind("email", email_input)
    state.bind("status", status_text)
    state.bind("user", user_text)


if __name__ == "__main__":
    ft.app(target=main)
