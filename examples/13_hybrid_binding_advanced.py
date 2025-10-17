"""
Example 13: Advanced Hybrid Binding Strategy

This example demonstrates the power of the hybrid binding strategy in Flet-ASP.
It shows how bindings work reliably regardless of when controls are added to the page.

Key Features Demonstrated:
1. Binding BEFORE adding controls to page (lazy updates)
2. Binding AFTER adding controls to page (immediate updates)
3. Dynamic control creation with bindings
4. Navigation with automatic state preservation
5. Custom controls with did_mount hooks
6. Responsive layout adapting to screen size
7. Dark/Light mode support
"""

import flet as ft
import flet_asp as fa


class DynamicCard(ft.Column):
    """Custom control demonstrating did_mount hook integration."""

    def __init__(self, page: ft.Page, title: str, value_key: str, color: str):
        super().__init__()
        self.page = page
        self.title = title
        self.value_key = value_key
        self.color = color
        self.value_text = ft.Ref[ft.Text]()

        self.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                ref=self.value_text, size=32, weight=ft.FontWeight.BOLD
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                elevation=2,
            )
        ]

    def did_mount(self):
        """This is called when the control is added to the page."""
        print(
            f"✅ DynamicCard '{self.title}' mounted - hybrid binding will update automatically!"
        )


def main(page: ft.Page):
    page.title = "Advanced Hybrid Binding Demo"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    state = fa.get_state_manager(page)

    # Initialize state
    state.atom("counter_a", 0)
    state.atom("counter_b", 0)
    state.atom("counter_c", 0)
    state.atom("demo_mode", "before")  # "before", "after", "dynamic"
    state.atom("theme_mode", "light")

    # Theme toggle
    theme_icon_ref = ft.Ref[ft.IconButton]()

    def toggle_theme(e):
        current = state.get("theme_mode")
        new_mode = "dark" if current == "light" else "light"
        state.set("theme_mode", new_mode)
        page.theme_mode = (
            ft.ThemeMode.DARK if new_mode == "dark" else ft.ThemeMode.LIGHT
        )
        theme_icon_ref.current.icon = (
            ft.Icons.LIGHT_MODE if new_mode == "dark" else ft.Icons.DARK_MODE
        )
        theme_icon_ref.current.tooltip = (
            f"Switch to {'light' if new_mode == 'dark' else 'dark'} mode"
        )
        page.update()

    # Set initial theme
    page.theme_mode = ft.ThemeMode.LIGHT
    state.set("theme_mode", "light")

    # Create refs for different scenarios
    before_ref = ft.Ref[ft.Text]()
    after_ref = ft.Ref[ft.Text]()

    # Info section
    info_text = ft.Ref[ft.Text]()

    def update_info(mode: str):
        """Update info text based on demo mode."""
        infos = {
            "before": (
                "🔵 BEFORE Mode: Controls are bound BEFORE being added to the page.\n"
                "This uses the hybrid strategy: lazy update → queue → flush on page.update()"
            ),
            "after": (
                "🟢 AFTER Mode: Controls are bound AFTER being added to the page.\n"
                "This is the fast path: immediate update (99% of cases)"
            ),
            "dynamic": (
                "🟡 DYNAMIC Mode: Custom controls with did_mount hooks.\n"
                "Hybrid strategy uses lifecycle hooks for automatic updates"
            ),
        }
        if info_text.current:
            info_text.current.value = infos.get(mode, "")
            page.update()

    # Scenario 1: Bind BEFORE adding to page
    def scenario_before(e):
        """Demonstrate binding before adding control."""
        state.set("demo_mode", "before")
        update_info("before")

        # IMPORTANT: Bind happens BEFORE control is added!
        print("\n🔵 Scenario 1: Binding BEFORE adding to page")
        print("   1. Creating state binding...")
        state.bind("counter_a", before_ref)
        print("   2. Control NOT yet added to page")
        print("   3. Hybrid strategy: property set (lazy), queued for retry")

        # Now add the control
        print("   4. Adding control to page...")
        content_area.current.content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Counter A (Bound BEFORE mount):",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(
                            content=ft.Text(
                                ref=before_ref, size=48, weight=ft.FontWeight.BOLD
                            ),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                        ft.ElevatedButton(
                            "Increment",
                            on_click=lambda e: state.set(
                                "counter_a", state.get("counter_a") + 1
                            ),
                            icon=ft.Icons.ADD,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(
                                    horizontal=30, vertical=15
                                ),
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
            ),
            elevation=2,
        )
        print("   5. Calling page.update()...")
        page.update()
        print("   6. ✅ Queue flushed, control updated automatically!")

    # Scenario 2: Bind AFTER adding to page
    def scenario_after(e):
        """Demonstrate binding after adding control (fast path)."""
        state.set("demo_mode", "after")
        update_info("after")

        print("\n🟢 Scenario 2: Binding AFTER adding to page (fast path)")
        print("   1. Adding control to page first...")
        content_area.current.content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Counter B (Bound AFTER mount):",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(
                            content=ft.Text(
                                ref=after_ref, size=48, weight=ft.FontWeight.BOLD
                            ),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                        ft.ElevatedButton(
                            "Increment",
                            on_click=lambda e: state.set(
                                "counter_b", state.get("counter_b") + 1
                            ),
                            icon=ft.Icons.ADD,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(
                                    horizontal=30, vertical=15
                                ),
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
            ),
            elevation=2,
        )
        page.update()

        print("   2. Now binding to already-mounted control...")
        state.bind("counter_b", after_ref)
        print("   3. ✅ Immediate update (zero latency)!")

    # Scenario 3: Dynamic custom controls with did_mount
    def scenario_dynamic(e):
        """Demonstrate dynamic control creation with did_mount hooks."""
        state.set("demo_mode", "dynamic")
        update_info("dynamic")

        print("\n🟡 Scenario 3: Dynamic custom controls with did_mount")
        print("   1. Creating 3 custom DynamicCard controls...")

        # Create dynamic cards
        colors = [ft.Colors.BLUE_700, ft.Colors.GREEN_700, ft.Colors.PURPLE_700]
        cards = []
        for i in range(3):
            card = DynamicCard(page, f"Card {i + 1}", "counter_c", colors[i])
            state.bind("counter_c", card.value_text)
            cards.append(card)
            print(f"   2. Bound Card {i + 1} (control not yet mounted)")

        print("   3. Adding all cards to page...")
        content_area.current.content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Dynamic Cards (with did_mount hooks):",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(height=10),
                        ft.ResponsiveRow(
                            [
                                ft.Container(card, col={"sm": 12, "md": 4, "lg": 4})
                                for card in cards
                            ],
                            spacing=15,
                            run_spacing=15,
                        ),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Increment All",
                            on_click=lambda e: state.set(
                                "counter_c", state.get("counter_c") + 1
                            ),
                            icon=ft.Icons.ADD,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(
                                    horizontal=30, vertical=15
                                ),
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=30,
            ),
            elevation=2,
        )
        print("   4. Calling page.update()...")
        page.update()
        print("   5. ✅ did_mount() called, all cards updated automatically!")

    # UI Layout
    content_area = ft.Ref[ft.Container]()

    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "🎯 Advanced Hybrid Binding Strategy",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "See how Flet-ASP handles bindings regardless of when controls are added",
                            size=14,
                            opacity=0.8,
                        ),
                    ],
                    expand=True,
                ),
                ft.IconButton(
                    ref=theme_icon_ref,
                    icon=ft.Icons.DARK_MODE,
                    tooltip="Switch to dark mode",
                    on_click=toggle_theme,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.PRIMARY),
        margin=ft.margin.only(bottom=20),
    )

    # Info panel
    info_panel = ft.Card(
        content=ft.Container(
            content=ft.Text(ref=info_text, size=14),
            padding=20,
        ),
        elevation=1,
    )

    # Scenario buttons
    buttons_row = ft.ResponsiveRow(
        [
            ft.Container(
                ft.ElevatedButton(
                    "🔵 Bind BEFORE",
                    on_click=scenario_before,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=25, vertical=15),
                    ),
                    expand=True,
                ),
                col={"sm": 12, "md": 4, "lg": 4},
            ),
            ft.Container(
                ft.ElevatedButton(
                    "🟢 Bind AFTER",
                    on_click=scenario_after,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=25, vertical=15),
                    ),
                    expand=True,
                ),
                col={"sm": 12, "md": 4, "lg": 4},
            ),
            ft.Container(
                ft.ElevatedButton(
                    "🟡 Dynamic Controls",
                    on_click=scenario_dynamic,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.ORANGE_700,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=25, vertical=15),
                    ),
                    expand=True,
                ),
                col={"sm": 12, "md": 4, "lg": 4},
            ),
        ],
        spacing=15,
        run_spacing=15,
    )

    # Content area
    content_container = ft.Container(
        ref=content_area,
        alignment=ft.alignment.center,
        height=400,
    )

    # Debug info
    debug_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.TERMINAL, size=20),
                            ft.Text(
                                "Console Output", size=16, weight=ft.FontWeight.BOLD
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(
                        "Check your console/terminal to see the hybrid strategy in action!",
                        size=12,
                        opacity=0.7,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        ),
        elevation=1,
    )

    page.add(
        ft.Column(
            [
                header,
                info_panel,
                ft.Container(height=10),
                buttons_row,
                ft.Container(height=10),
                content_container,
                ft.Container(height=10),
                debug_card,
            ],
            spacing=0,
        )
    )

    # Show initial scenario
    scenario_before(None)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Advanced Hybrid Binding Demo")
    print("=" * 60)
    print("\nWatch the console for detailed step-by-step execution!\n")
    ft.app(target=main)
