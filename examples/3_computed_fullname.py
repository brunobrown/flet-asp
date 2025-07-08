import flet as ft
import fasp as fa


def main(page: ft.Page):
    state = fa.get_state_manager(page)

    state.set("first_name", "")
    state.set("last_name", "")

    @state.computed("full_name")
    def full_name(get):
        return f"{get('first_name')} {get('last_name')}".strip()

    # OR
    #
    # state.add_computed(
    #     "full_name",
    #     lambda get: f"{get('first_name')} {get('last_name')}".strip()
    # )

    first_ref = ft.Ref[ft.TextField]()
    last_ref = ft.Ref[ft.TextField]()
    full_ref = ft.Ref[ft.Text]()

    page.add(
        ft.Text(ref=full_ref),
        ft.TextField(label="Nome", ref=first_ref, on_change=lambda e: state.set("first_name", e.control.value)),
        ft.TextField(label="Sobrenome", ref=last_ref, on_change=lambda e: state.set("last_name", e.control.value)),
    )

    state.bind("full_name", full_ref)


if __name__ == "__main__":
    ft.app(target=main)
