"""
Example 15: Atomic Design with Dynamic Theming

A component library showcase demonstrating:
- Theme tokens as design system foundation
- Reactive theme switching with flet-asp
- Theme-aware atoms and molecules
- Scalable design system architecture

This example shows how professional design systems handle theming
and how flet-asp state management enables real-time theme updates
across entire component hierarchies.

Run this example:
    python examples/15_atomic_design_theming/main.py

Or as a module:
    python -m examples.15_atomic_design_theming.main
"""

import flet as ft
import flet_asp as fa

# Handle both direct execution and module import
try:
    from . import atoms, molecules
    from .theme_tokens import get_theme
except ImportError:
    import atoms
    import molecules
    from theme_tokens import get_theme


def main(page: ft.Page):
    """Main application entry point."""
    page.title = "Atomic Design - Theming"
    page.padding = 0

    # Initialize state and theme
    fa.get_state_manager(page)
    theme = get_theme()

    # ========================================================================
    # STATE ATOMS
    # ========================================================================

    page.state.atom("theme_mode", "light")
    page.state.atom("user_count", "2,345")
    page.state.atom("revenue", "$89,432")
    page.state.atom("active_users", "892")

    # ========================================================================
    # REBUILD FUNCTION
    # ========================================================================

    def rebuild_ui():
        """Rebuild entire UI with current theme."""
        current_mode = page.state.get("theme_mode")
        theme.mode = current_mode

        # Update page background
        page.bgcolor = theme.colors.background

        # Clear and rebuild
        page.controls.clear()

        # ====================================================================
        # HEADER SECTION
        # ====================================================================

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            atoms.icon(ft.Icons.PALETTE, size=32, semantic="primary"),
                            atoms.headline_text("Design System", level=2),
                        ],
                        spacing=theme.spacing.md,
                    ),
                    ft.Container(expand=True),
                    molecules.theme_toggle(
                        current_mode=current_mode,
                        on_toggle=lambda e: toggle_theme(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=theme.spacing.xl,
            bgcolor=theme.colors.surface,
            border=ft.border.only(bottom=ft.BorderSide(1, theme.colors.border)),
        )

        # ====================================================================
        # MAIN CONTENT
        # ====================================================================

        content = ft.Column(
            [
                # Welcome section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.display_text("Component Library"),
                            atoms.body_text(
                                "A showcase of theme-aware components built with Atomic Design principles",
                                secondary=True,
                            ),
                        ],
                        spacing=theme.spacing.sm,
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # Stats section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("Dashboard Metrics", level=1),
                            ft.Container(height=theme.spacing.md),
                            ft.ResponsiveRow(
                                [
                                    ft.Container(
                                        molecules.stat_card(
                                            "Total Users",
                                            page.state.get("user_count"),
                                            ft.Icons.PEOPLE,
                                            "+12.5%",
                                            True,
                                        ),
                                        col={"sm": 12, "md": 6, "lg": 4},
                                    ),
                                    ft.Container(
                                        molecules.stat_card(
                                            "Revenue",
                                            page.state.get("revenue"),
                                            ft.Icons.ATTACH_MONEY,
                                            "+8.3%",
                                            True,
                                        ),
                                        col={"sm": 12, "md": 6, "lg": 4},
                                    ),
                                    ft.Container(
                                        molecules.stat_card(
                                            "Active Now",
                                            page.state.get("active_users"),
                                            ft.Icons.ONLINE_PREDICTION,
                                            "-2.1%",
                                            False,
                                        ),
                                        col={"sm": 12, "md": 12, "lg": 4},
                                    ),
                                ],
                                spacing=theme.spacing.lg,
                            ),
                        ],
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # Alerts section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("Alerts", level=1),
                            ft.Container(height=theme.spacing.md),
                            molecules.alert(
                                "Operation completed successfully!", "success", True
                            ),
                            molecules.alert(
                                "Please review your settings.", "warning", True
                            ),
                            molecules.alert(
                                "An error occurred while processing.", "error", True
                            ),
                            molecules.alert("New updates are available.", "info", True),
                        ],
                        spacing=theme.spacing.md,
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # Buttons section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("Buttons", level=1),
                            ft.Container(height=theme.spacing.md),
                            ft.Row(
                                [
                                    atoms.filled_button(
                                        "Filled Button", icon=ft.Icons.ADD
                                    ),
                                    atoms.outlined_button(
                                        "Outlined Button", icon=ft.Icons.EDIT
                                    ),
                                    atoms.text_button(
                                        "Text Button", icon=ft.Icons.OPEN_IN_NEW
                                    ),
                                    atoms.icon_button(
                                        ft.Icons.FAVORITE, tooltip="Favorite"
                                    ),
                                ],
                                spacing=theme.spacing.md,
                                wrap=True,
                            ),
                        ],
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # Form section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("Form Elements", level=1),
                            ft.Container(height=theme.spacing.md),
                            ft.ResponsiveRow(
                                [
                                    ft.Container(
                                        molecules.input_group(
                                            "Full Name",
                                            help_text="Enter your full name",
                                        ),
                                        col={"sm": 12, "md": 6},
                                    ),
                                    ft.Container(
                                        molecules.input_group(
                                            "Email Address",
                                            help_text="We'll never share your email",
                                        ),
                                        col={"sm": 12, "md": 6},
                                    ),
                                ],
                                spacing=theme.spacing.lg,
                            ),
                            ft.Container(height=theme.spacing.md),
                            ft.Row(
                                [
                                    atoms.checkbox("Accept terms and conditions"),
                                    atoms.checkbox("Subscribe to newsletter"),
                                ],
                                spacing=theme.spacing.lg,
                                wrap=True,
                            ),
                        ],
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # List section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("List Items", level=1),
                            ft.Container(height=theme.spacing.md),
                            atoms.card(
                                content=ft.Column(
                                    [
                                        molecules.list_item(
                                            "John Doe",
                                            "Software Engineer",
                                            ft.Icons.PERSON,
                                            molecules.avatar("John Doe", size=32),
                                        ),
                                        molecules.list_item(
                                            "Jane Smith",
                                            "Product Manager",
                                            ft.Icons.PERSON,
                                            molecules.avatar("Jane Smith", size=32),
                                        ),
                                        molecules.list_item(
                                            "Bob Johnson",
                                            "UI/UX Designer",
                                            ft.Icons.PERSON,
                                            molecules.avatar("Bob Johnson", size=32),
                                        ),
                                    ],
                                    spacing=0,
                                ),
                            ),
                        ],
                    ),
                    padding=theme.spacing.xl,
                ),
                atoms.divider(),
                # Badges section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.title_text("Badges & Chips", level=1),
                            ft.Container(height=theme.spacing.md),
                            ft.Row(
                                [
                                    molecules.badge("Success", "success"),
                                    molecules.badge("Warning", "warning"),
                                    molecules.badge("Error", "error"),
                                    molecules.badge("Info", "info"),
                                    molecules.badge("Default"),
                                ],
                                spacing=theme.spacing.md,
                                wrap=True,
                            ),
                            ft.Container(height=theme.spacing.md),
                            ft.Row(
                                [
                                    atoms.chip("React"),
                                    atoms.chip("Vue"),
                                    atoms.chip("Angular"),
                                    atoms.chip("Flet"),
                                ],
                                spacing=theme.spacing.sm,
                                wrap=True,
                            ),
                        ],
                    ),
                    padding=theme.spacing.xl,
                ),
                # Footer
                ft.Container(
                    content=atoms.body_text(
                        "Built with Flet-ASP and Atomic Design principles",
                        secondary=True,
                    ),
                    padding=theme.spacing.xl,
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # ====================================================================
        # ADD TO PAGE
        # ====================================================================

        page.add(
            ft.Column(
                [header, content],
                spacing=0,
                expand=True,
            )
        )

        page.update()

    # ========================================================================
    # THEME TOGGLE HANDLER
    # ========================================================================

    def toggle_theme():
        """Toggle between light and dark mode."""
        current = page.state.get("theme_mode")
        new_mode = "dark" if current == "light" else "light"
        page.state.set("theme_mode", new_mode)
        rebuild_ui()

    # ========================================================================
    # LISTEN TO THEME CHANGES
    # ========================================================================

    page.state.listen("theme_mode", lambda mode: None, immediate=False)

    # ========================================================================
    # INITIAL RENDER
    # ========================================================================

    rebuild_ui()


if __name__ == "__main__":
    ft.app(target=main)
