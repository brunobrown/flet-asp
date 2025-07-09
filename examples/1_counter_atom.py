import flet as ft
import fasp as fa


def main(page: ft.Page):
    # Get or create a global reactive state for this page
    state: fa.StateManager = fa.get_state_manager(page)

    # Create an atom named 'count' with initial value 0
    state.atom("count", 0)

    # Create a Ref for the Text control
    count_text_ref = ft.Ref[ft.Text]()
    count_text = ft.Text(ref=count_text_ref)

    # Define increment logic
    def increment(e):
        state.set("count", state.get("count") + 1)

    # Define decrement logic
    def decrement(e):
        state.set("count", state.get("count") - 1)

    # Add the UI controls to the page
    page.add(
        count_text,
        ft.Row(
            controls=[
                ft.ElevatedButton(text="Increment", on_click=increment),
                ft.ElevatedButton(text="Decrement", on_click=decrement),
            ]
        )
    )

    # Bind the 'count' atom to the Text control using the ref
    # Must be called after the control is on the page
    state.bind("count", count_text_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
