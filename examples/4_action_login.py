import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    """
    This example demonstrates how to use the Action class in FASP to encapsulate an asynchronous operation, such as a login request.
    It simulates a simple authentication form that updates UI state reactively:

    - A loading spinner is shown during login
    - If credentials are valid, user info is displayed
    - If invalid, an error message appears
    """

    # Get or create the page-specific state manager
    state: fa.StateManager = fa.get_state_manager(page)

    # Declare reactive atoms to hold UI and app state
    state.atom("email", "")
    state.atom("password", "")
    state.atom("user", None)
    state.atom("loading", False)
    state.atom("error", "")

    # Create UI control references for binding
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    user_ref = ft.Ref[ft.Text]()
    error_ref = ft.Ref[ft.Text]()
    loading_ref = ft.Ref[ft.ProgressRing]()

    # Define the login action logic (asynchronous)
    async def login_action(get, set_value, args):
        set_value("loading", True)
        set_value("error", "")

        # Simulate an API delay
        await asyncio.sleep(1.5)

        # Read current values from state
        email = get("email")
        password = get("password")

        # Simulated credential validation
        if email == "test@test.com" and password == "123":
            set_value("user", {"email": email})
        else:
            set_value("error", "Invalid credentials")
            set_value("user", None)

        set_value("loading", False)

    # Create the Action object
    login = fa.Action(login_action)

    # Run the action when the login button is clicked
    async def on_login_click(e):
        await login.run_async(state)

    # Build the page layout
    page.add(
        ft.Column([
            ft.TextField(
                label="Email",
                ref=email_ref,
                on_change=lambda e: state.set("email", e.control.value)
            ),
            ft.TextField(
                label="Password",
                password=True,
                ref=password_ref,
                on_change=lambda e: state.set("password", e.control.value)
            ),
            ft.ElevatedButton("Login", on_click=on_login_click),
            ft.ProgressRing(ref=loading_ref),
            ft.Text(ref=error_ref, color="red"),
            ft.Text(ref=user_ref, color="green"),
        ])
    )

    # Bind state values to UI controls
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref, prop="value")
    state.bind("user", user_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
