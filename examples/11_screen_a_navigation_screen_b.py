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
    count_ref = ft.Ref[ft.Text]()

    def go_back(e):
        page.go("/")

    view = ft.View(
        "/b",
        [
            ft.Text("Screen B — Count is still: ", spans=[ft.TextSpan(ref=count_ref)]),
            ft.ElevatedButton("Go back", on_click=go_back),
        ],
    )

    # Bind count to show current value reactively
    page.state.bind("count", count_ref, prop="text")
    return view


def main(page: ft.Page):
    """
    App entry point.

    Navigation pattern using page.views stack.
    Note: page.go() triggers on_route_change which modifies page.views.
    page.update() is required by Flet after modifying page.views.
    """
    fa.get_state_manager(page)
    page.state.atom("count", 0)

    def route_change(e):
        # Clear views and rebuild based on route
        page.views.clear()

        if page.route == "/b":
            page.views.append(screen_b(page))
        else:
            page.views.append(screen_a(page))

        # Required by Flet when manually modifying page.views for navigation
        # This is a Flet requirement, not related to Flet-ASP state management
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1] if page.views else None
        if top_view:
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
