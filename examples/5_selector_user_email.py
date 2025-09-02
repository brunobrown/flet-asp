import asyncio
import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example demonstrates how to use a Selector in Flet-ASP to derive and listen to a specific property inside an object (in this case, user["email"]).
    Instead of binding the entire user atom, this approach focuses only on what matters — the email.
    The derived value is updated and applied without using bind(), via a manual update.

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

    # Define the async login action
    async def login_action(get, set_value, _):
        set_value("loading", True)
        set_value("error", "")
        await asyncio.sleep(1)

        if get("email") == "test@test.com" and get("password") == "123":
            set_value("user", {"email": get("email")})
        else:
            set_value("error", "Invalid login")
            set_value("user", None)

        set_value("loading", False)

    # Create the action instance
    login = fa.Action(login_action)

    # Trigger login on button click
    async def on_login_click(e):
        await login.run_async(state)

    # Selector that watches only the user's email
    user_email_selector = fa.Selector(
        resolve_atom=state.atom,
        select_fn=lambda get: (get("user") or {}).get("email", ""),
    )

    # Update the Text control manually when the selector changes
    def update_email_text(value):
        email_text_ref.current.value = value
        email_text_ref.current.update()

    # Listen to the selector and apply changes to the control
    user_email_selector.listen(
        callback=update_email_text,
        immediate=False,  # skip first call (optional)
    )

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

    # Bind loading and error states to controls
    state.bind("loading", loading_ref, prop="visible")
    state.bind("error", error_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
