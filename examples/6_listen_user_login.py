import asyncio
import flet as ft
import fasp as fa


def main(page: ft.Page):
    """
    This example shows how to use the listen() method in FASP to observe changes to a specific atom ("user"), and trigger side effects such as manual UI updates.
    Instead of binding a control directly to a value (bind()), it listens to a state and reacts accordingly.

    * User types credentials and clicks Login
    * Simulated async login updates a label with a progress counter
    * After login:
        - If valid: shows Welcome, <email>
        - If invalid: shows User not authenticated
    """

    # Get or create the page-specific state manager
    state = fa.get_state_manager(page)

    # Declare base atoms
    state.atom("email", "")
    state.atom("password", "")
    state.atom("user", None)

    # UI control references
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    welcome_ref = ft.Ref[ft.Text]()

    # Define the async login action
    async def login_action(get, set_value, _):
        # Simulate loading step
        for i in range(10):
            await asyncio.sleep(0.1)
            welcome_ref.current.value = f"Authenticating... {i}"
            welcome_ref.current.update()

        # Fake credential validation
        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
        else:
            set_value("user", None)

    # Create the action
    login = fa.Action(login_action)

    # Run the action when the button is clicked
    async def on_login_click(e):
        await login.run_async(state)

    # React to changes in the "user" atom
    def on_user_change(user_data):
        if user_data:
            welcome_ref.current.value = f"Welcome, {user_data['email']}!"
        else:
            welcome_ref.current.value = "User not authenticated."
        welcome_ref.current.update()

    # Build the UI
    page.add(
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
        ft.Text(ref=welcome_ref)
    )

    # Listen to the "user" atom and reactively update the welcome message
    state.listen("user", on_user_change)


if __name__ == "__main__":
    ft.app(target=main)
