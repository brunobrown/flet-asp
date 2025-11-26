import asyncio
import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example shows how to use listen() in Flet-ASP for side effects,
    combined with @selector for derived state and @action for async operations.

    Key concepts demonstrated:
    - @action decorator for async login workflow
    - @selector decorator for derived welcome message
    - listen() for side effects (console logging)
    - bind() for declarative UI updates

    * User types credentials and clicks Login
    * Simulated async login with progress updates
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
    state.atom("auth_status", "")  # For progress messages during login

    # UI control references
    email_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    welcome_ref = ft.Ref[ft.Text]()

    # Define the async login action using @action decorator
    @state.action
    async def login(get, set_value):
        # Simulate loading step with progress updates
        for i in range(10):
            await asyncio.sleep(0.1)
            set_value("auth_status", f"Authenticating... {i}")

        # Fake credential validation
        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
            set_value("auth_status", "")  # Clear status on success
        else:
            set_value("user", None)
            set_value("auth_status", "")  # Clear status on failure

    # Run the action when the button is clicked
    def on_login_click(e):
        page.run_task(login)

    # Selector that derives the welcome message from user and auth_status
    @state.selector("welcome_message")
    def get_welcome_message(get):
        auth_status = get("auth_status")
        if auth_status:
            return auth_status  # Show progress during authentication

        user = get("user")
        if user:
            return f"Welcome, {user['email']}!"
        return "User not authenticated."

    # Listen for side effects (e.g., logging) - this is what listen() is best for
    def on_user_change(user_data):
        if user_data:
            print(f"[Analytics] User logged in: {user_data['email']}")
        else:
            print("[Analytics] User logged out or login failed")

    # Build the UI
    page.add(
        ft.TextField(
            label="Email",
            ref=email_ref,
            on_change=lambda e: state.set("email", e.control.value),
        ),
        ft.TextField(
            label="Password",
            password=True,
            ref=password_ref,
            on_change=lambda e: state.set("password", e.control.value),
        ),
        ft.ElevatedButton("Login", on_click=on_login_click),
        ft.Text(ref=welcome_ref),
    )

    # Bind the selector to the welcome text - fully declarative!
    state.bind("welcome_message", welcome_ref, prop="value")

    # Listen for side effects (logging, analytics, etc.)
    state.listen("user", on_user_change, immediate=False)


if __name__ == "__main__":
    ft.app(target=main)
