import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example demonstrates how to define a derived state in FletASP using the @selector(...) decorator.
    The selector named "full_name" is built from two base atoms: "first_name" and "last_name".

    Whenever either atom changes, the selector is automatically recomputed, and the UI is updated reactively.

    - The user types into the first name and last name fields
    - The full name text updates automatically and reactively
    - No need for manual updates or imperative logic
    """

    # Create or retrieve the FletASP state manager for this page
    state = fa.get_state_manager(page)

    # Declare two base atoms for first and last name
    state.atom("first_name", "")
    state.atom("last_name", "")

    # Declare a derived state (selector) that depends on the above atoms
    @state.selector("full_name")
    def full_name(get):
        # get("key") retrieves the current value of any atom or selector
        return f"{get('first_name')} {get('last_name')}".strip()

    # Alternatively, using function registration:
    # state.add_selector(
    #     "full_name",
    #     lambda get: f"{get('first_name')} {get('last_name')}".strip()
    # )

    # Create references for the UI controls
    full_ref = ft.Ref[ft.Text]()
    first_ref = ft.Ref[ft.TextField]()
    last_ref = ft.Ref[ft.TextField]()

    # Build the UI layout
    page.add(
        ft.Text(ref=full_ref),  # Displays the full name
        ft.TextField(
            label="First name",
            ref=first_ref,
            on_change=lambda e: state.set("first_name", e.control.value),
        ),
        ft.TextField(
            label="Last name",
            ref=last_ref,
            on_change=lambda e: state.set("last_name", e.control.value),
        ),
    )

    # Bind the "full_name" selector to the Text control
    state.bind("full_name", full_ref)


if __name__ == "__main__":
    ft.app(target=main)
