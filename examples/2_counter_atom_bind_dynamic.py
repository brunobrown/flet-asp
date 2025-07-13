import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    Basic Counter using Atom and bind_dynamic() without Ref

    This example demonstrates how to use Flet-ASP's bind_dynamic() to connect an Atom state directly to a UI control, without using a Ref.
    It is similar to the previous example, but uses direct control reference instead of Ref. This is often more convenient and readable for small UIs.

    - A Text widget displays the current "count" value
    - Two buttons increment and decrement the value
    - The value is updated automatically via reactive state
    """

    page.title = "Flet-ASP Counter Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Create or retrieve a unique state manager for this page
    state: fa.StateManager = fa.get_state_manager(page)

    # Declare a reactive atom named 'count' with initial value 0
    state.atom("count", 0)

    # Direct control, no Ref needed
    count_text = ft.TextField(width=100, text_align=ft.TextAlign.RIGHT)

    # Define increment logic
    def increment(e):
        state.set("count", state.get("count") + 1)

    # Define decrement logic
    def decrement(e):
        state.set("count", state.get("count") - 1)

    # Build the UI
    page.add(
        ft.Column(
            controls=[
                count_text,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("-", on_click=decrement),
                        ft.ElevatedButton("+", on_click=increment),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Bind the 'count' atom directly to the Text's 'value' property
    state.bind_dynamic("count", count_text, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
