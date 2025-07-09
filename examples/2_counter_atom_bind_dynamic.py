import flet as ft
import fasp as fa


def main(page: ft.Page):
    # Create or retrieve a unique state manager for this page
    state: fa.StateManager = fa.get_state_manager(page)

    # Declare a reactive atom named 'count' with initial value 0
    state.atom("count", 0)

    # Direct control, no Ref needed
    count_text = ft.Text()

    # Define increment logic
    def increment(e):
        state.set("count", state.get("count") + 1)

    # Define decrement logic
    def decrement(e):
        state.set("count", state.get("count") - 1)

    # Build the UI
    page.add(
        count_text,
        ft.Row(
            controls=[
                ft.ElevatedButton(text="Increment", on_click=increment),
                ft.ElevatedButton(text="Decrement", on_click=decrement),
            ]
        )
    )

    # Bind the 'count' atom directly to the Text's 'value' property
    state.bind_dynamic("count", count_text, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
