import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    """
    Basic Counter using Atom and bind() with Ref

    - Atom: a named reactive state (“count”)
    - bind(): link between the state and a UI component via Ref
    - Increment and decrement controls
    """

    page.title = "Flet-ASP Counter Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Get or create a global reactive state for this page
    state = fa.get_state_manager(page)

    # Create an atom named 'count' with initial value 0
    state.atom("count", 0)

    # Create a Ref for the Text control
    text_number_ref = ft.Ref[ft.TextField]()
    text_number = ft.TextField(ref=text_number_ref, text_align=ft.TextAlign.RIGHT, width=100)

    # Define increment logic
    def minus_click(e):
        state.set("count", state.get("count") - 1)

    # Define decrement logic
    def plus_click(e):
        state.set("count", state.get("count") + 1)

    # Add the UI controls to the page
    page.add(
        ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.REMOVE, on_click=minus_click),
                text_number,
                ft.IconButton(icon=ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    # Bind the 'count' atom to the Text control using the ref
    # Must be called after the control is on the page
    state.bind("count", text_number_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
