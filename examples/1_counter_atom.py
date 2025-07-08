import flet as ft
import fasp as fa


def main(page: ft.Page):
    state: fa.StateManager = fa.get_state_manager(page)

    # Cria um atom chamado 'count'
    state.set("count", 0)

    # Ref para o controle Text
    count_text_ref = ft.Ref[ft.Text]()
    count_text = ft.Text(ref=count_text_ref)

    def increment(e):
        state.set("count", state.get("count") + 1)

    def decrement(e):
        state.set("count", state.get("count") - 1)

    # Cria a UI com o Text usando ref
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
    state.bind("count", count_text_ref, prop="value")


if __name__ == "__main__":
    ft.app(target=main)
