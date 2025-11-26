import asyncio
import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example demonstrates how to use the @selector decorator in Flet-ASP
    to derive a specific property from an object (in this case, user["email"]).

    Instead of binding the entire user atom, this approach focuses only on
    what matters — the email. The derived value is updated automatically
    via bind() - no manual update needed!

    * The user types in credentials and clicks Login
    * If login is successful:
        - A green label displays the user's email

    * If login fails:
        - An error message is shown
        - The email label remains empty

    """

    # Create the Flet-ASP state manager for this page
    state: fa.StateManager = fa.get_state_manager(page)

    # Declare base atoms
    state.atom("email", "")
    state.atom("password", "")
    state.atom("user", None)
    state.atom("loading", False)
    state.atom("error", "")

    # UI references
    email_input_ref = ft.Ref[ft.TextField]()
    pass_input_ref = ft.Ref[ft.TextField]()
    error_ref = ft.Ref[ft.Text]()
    email_text_ref = ft.Ref[ft.Text]()
    loading_ref = ft.Ref[ft.ProgressRing]()

    # Define the async login action using @action decorator
    @state.action
    async def login(get, set_value):
        set_value("loading", True)
        set_value("error", "")
        await asyncio.sleep(1)

        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
        else:
            set_value("error", "Invalid login")
            set_value("user", None)

        set_value("loading", False)

    # Trigger login on button click
    def on_login_click(e):
        page.run_task(login)

    # Selector that derives only the user's email from the user object
    # This is more efficient than watching the entire user object
    @state.selector("user_email")
    def get_user_email(get):
        user = get("user")
        return (user or {}).get("email", "")

    # Build the UI layout
    page.add(
        ft.TextField(
            label="Email",
            ref=email_input_ref,
            on_change=lambda e: state.set("email", e.control.value),
        ),
        ft.TextField(
            label="Password",
            password=True,
            ref=pass_input_ref,
            on_change=lambda e: state.set("password", e.control.value),
        ),
        ft.ElevatedButton("Login", on_click=on_login_click),
        ft.ProgressRing(ref=loading_ref),
        ft.Text(ref=error_ref, color="red"),
        ft.Text(ref=email_text_ref, color="green"),  # updated by Selector
    )

    # Bind states to controls - fully declarative, no manual update needed!
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref, prop="value")
    state.bind("user_email", email_text_ref, prop="value")  # Bind selector to text


if __name__ == "__main__":
    ft.app(target=main)
