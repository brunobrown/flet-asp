import flet as ft
import fasp as fa


def main(page: ft.Page):
    state: fa.StateManager = fa.get_state_manager(page)

    # Cria um atom chamado 'count'
    state.set("count", 0)

    count_text = ft.Text()

    def increment(e):
        state.set("count", state.get("count") + 1)

    def decrement(e):
        state.set("count", state.get("count") - 1)

    page.add(
        count_text,
        ft.Row(
            controls=[
                ft.ElevatedButton(text="increment", on_click=increment),
                ft.ElevatedButton(text="decrement", on_click=decrement),
            ]
        )
    )

    # Faz o vínculo após o Text estar adicionado à página
    state.bind_dynamic("count", count_text, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
