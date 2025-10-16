import flet as ft
import flet_asp as fa


def screen_a(page: ft.Page):
    """Main screen with a counter and navigation to screen B."""
    count_ref = ft.Ref[ft.Text]()

    def increment(e):
        page.state.set("count", page.state.get("count") + 1)

    def go_to_b(e):
        page.go("/b")

    # A view returns its layout directly
    view = ft.View(
        "/",
        [
            ft.Text(ref=count_ref),
            ft.ElevatedButton("Increment", on_click=increment),
            ft.ElevatedButton("Go to Screen B", on_click=go_to_b),
        ],
    )

    # Bind the count atom to the text control
    page.state.bind("count", count_ref)
    return view


def screen_b(page: ft.Page):
    """Secondary screen displaying the same counter."""

    def go_back(e):
        page.go("/")

    return ft.View(
        "/b",
        [
            ft.Text(f"Screen B — Count is still: {page.state.get('count')}"),
            ft.ElevatedButton("Go back", on_click=go_back),
        ],
    )


def main(page: ft.Page):
    """App entry point."""
    fa.get_state_manager(page)
    page.state.atom("count", 0)

    def route_change(e):
        # Clear views before switching
        page.views.clear()

        if page.route == "/b":
            page.views.append(screen_b(page))
        else:
            page.views.append(screen_a(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
