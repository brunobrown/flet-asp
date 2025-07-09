import flet as ft
import fasp as fa


def main(page: ft.Page):
    # Create or retrieve the page-specific state manager
    state = fa.get_state_manager(page)

    # Declare base atoms
    state.atom("first_name", "")
    state.atom("last_name", "")

    # Declare a computed atom derived from first and last name
    @state.computed("full_name")
    def full_name(get):
        return f"{get('first_name')} {get('last_name')}".strip()

    # Alternatively, using function:
    # state.add_computed(
    #     "full_name",
    #     lambda get: f"{get('first_name')} {get('last_name')}".strip()
    # )

    # Create references to the input and output controls
    first_ref = ft.Ref[ft.TextField]()
    last_ref = ft.Ref[ft.TextField]()
    full_ref = ft.Ref[ft.Text]()

    # Build the UI
    page.add(
        ft.Text(ref=full_ref),
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

    # Bind the computed value to the Text control
    state.bind("full_name", full_ref)


if __name__ == "__main__":
    ft.app(target=main)
