"""
Example 11.1: Global State Outside Page Scope

This example demonstrates how to create a global StateManager OUTSIDE the page scope.
Some developers need this pattern for sharing state across multiple page instances,
for testing, or for advanced state management scenarios.

Based on Example 11 (Screen A Navigation Screen B), but with global state.

Key Differences:
- StateManager created globally (not via page.state)
- Must manually attach page to the StateManager
- State persists across page instances
- Useful for: testing, multi-window apps, or advanced state management patterns

Run this example:
    python examples/11.1_global_state_outside.py
"""

import flet as ft
import flet_asp as fa


# ============================================================================
# GLOBAL STATE - Created OUTSIDE page scope
# ============================================================================

# Create a global StateManager instance
global_state = fa.StateManager()


# ============================================================================
# SCREEN DEFINITIONS
# ============================================================================


def screen_a(page: ft.Page):
    """Main screen with a counter and navigation to screen B."""
    count_ref = ft.Ref[ft.Text]()

    def increment(e):
        # Use global_state instead of page.state
        global_state.set("count", global_state.get("count") + 1)

    def go_to_b(e):
        page.go("/b")

    # A view returns its layout directly
    view = ft.View(
        "/",
        [
            ft.Text(
                "Screen A - Global State Example", size=24, weight=ft.FontWeight.BOLD
            ),
            ft.Divider(),
            ft.Text("Counter value:", size=16),
            ft.Text(
                ref=count_ref,
                size=40,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Container(height=20),
            ft.ElevatedButton("Increment", on_click=increment, icon=ft.Icons.ADD),
            ft.ElevatedButton(
                "Go to Screen B", on_click=go_to_b, icon=ft.Icons.ARROW_FORWARD
            ),
        ],
        padding=20,
    )

    # Bind using global_state instead of page.state
    global_state.bind("count", count_ref)
    return view


def screen_b(page: ft.Page):
    """Secondary screen displaying the same counter."""

    def go_back(e):
        page.go("/")

    return ft.View(
        "/b",
        [
            ft.Text(
                "Screen B - Global State Example", size=24, weight=ft.FontWeight.BOLD
            ),
            ft.Divider(),
            ft.Text(
                f"The counter value from Screen A is: {global_state.get('count')}",
                size=16,
            ),
            ft.Text(
                "✨ Notice: State is managed globally, outside the page!",
                size=14,
                color=ft.Colors.GREEN_700,
                italic=True,
            ),
            ft.Container(height=20),
            ft.ElevatedButton(
                "Go back to Screen A", on_click=go_back, icon=ft.Icons.ARROW_BACK
            ),
        ],
        padding=20,
    )


# ============================================================================
# MAIN APP
# ============================================================================


def main(page: ft.Page):
    """App entry point."""
    page.title = "Global State Outside Page"
    page.theme_mode = ft.ThemeMode.LIGHT

    # IMPORTANT: Attach the page to the global StateManager
    # This is required for bindings to work properly
    global_state.page = page

    # Initialize the count atom in global state
    global_state.atom("count", 0)

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
