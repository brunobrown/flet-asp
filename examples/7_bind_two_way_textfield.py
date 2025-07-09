import flet as ft
import fasp as fa


def main(page: ft.Page):
    state = fa.get_state_manager(page)

    # Atom com valor inicial
    state.atom("message", "Olá, mundo!")

    # Ref do campo de texto
    text_input_ref = ft.Ref[ft.TextField]()

    # Adiciona o controle à UI
    page.add(
        ft.TextField(ref=text_input_ref, label="Mensagem"),
        ft.ElevatedButton("Resetar", on_click=lambda e: state.reset("message", "Olá, mundo!")),
        ft.ElevatedButton("Limpar", on_click=lambda e: state.reset("message", "")),
    )

    def current_message(new_value):
        print("Valor atual no estado:", new_value)

    # Faz o binding bidirecional (estado <-> UI)
    state.bind_two_way("message", text_input_ref)

    state.listen('message', current_message)



if __name__ == "__main__":
    ft.app(target=main)

