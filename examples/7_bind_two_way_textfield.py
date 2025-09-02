import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    This example demonstrates how to use bind_two_way() in Flet-ASP to create a synchronized link between a UI control (TextField) and an atom. Any change in:
        * the input field updates the atom
        * the atom value updates the input field

    This is especially useful for inputs, sliders, switches, and any control where user input needs to directly influence state — and vice versa.

    - When user types in the field, the atom message updates automatically
    - When the atom is reset (via button), the UI is updated accordingly
    - Console prints the current value whenever it changes
    """

    # Get the page-specific Flet-ASP state manager
    state = fa.get_state_manager(page)

    # Declare the message atom with an initial value
    state.atom("message", "Hello, world!")

    # Create a reference to the TextField
    text_input_ref = ft.Ref[ft.TextField]()

    # Add the controls to the UI
    page.add(
        ft.TextField(ref=text_input_ref, label="Message"),
        ft.ElevatedButton(
            "Reset", on_click=lambda e: state.reset("message", "Hello, world!")
        ),
        ft.ElevatedButton("Clear", on_click=lambda e: state.reset("message", "")),
    )

    # This function is called whenever the atom changes
    def current_message(new_value):
        print("Current value:", new_value)

    # Establish two-way binding between the atom and the TextField
    state.bind_two_way("message", text_input_ref)

    # Listen to the atom to react programmatically (e.g., logging)
    state.listen("message", current_message)


if __name__ == "__main__":
    ft.app(target=main)
