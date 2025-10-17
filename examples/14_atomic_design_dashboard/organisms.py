"""
Organisms: Complex UI components composed of molecules, atoms, and other organisms.

Organisms form distinct sections of an interface and can stand alone as
functional units. They're more complex than molecules and often contain business logic.
"""

import flet as ft

# Handle both direct execution and module import
try:
    from . import atoms, molecules
except ImportError:
    import atoms
    import molecules


# ============================================================================
# SIDEBAR ORGANISM
# ============================================================================


def sidebar(page: ft.Page, current_view: str = "dashboard") -> ft.Container:
    """
    Sidebar organism: Complete navigation sidebar.

    Composed of:
    - Heading2 atom (logo/title)
    - Multiple menu item molecules
    - Horizontal divider atoms
    - User avatar molecule
    """

    def create_menu_item(icon: str, label: str, view: str):
        return molecules.menu_item(
            icon,
            label,
            selected=(current_view == view),
            on_click=lambda _: page.state.set("current_view", view),
        )

    return ft.Container(
        content=ft.Column(
            [
                # Logo section
                ft.Container(
                    content=ft.Row(
                        [
                            atoms.icon(
                                ft.Icons.DASHBOARD, size=32, color=ft.Colors.WHITE
                            ),
                            atoms.heading2("DashBoard", color=ft.Colors.WHITE),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                ),
                atoms.horizontal_divider(color=ft.Colors.BLUE_800),
                # Navigation section
                ft.Container(
                    content=ft.Column(
                        [
                            atoms.caption_text("MAIN MENU", color=ft.Colors.GREY_500),
                            ft.Container(height=10),
                            create_menu_item(ft.Icons.HOME, "Dashboard", "dashboard"),
                            create_menu_item(
                                ft.Icons.BAR_CHART, "Analytics", "analytics"
                            ),
                            create_menu_item(ft.Icons.PEOPLE, "Users", "users"),
                            create_menu_item(
                                ft.Icons.SHOPPING_CART, "Orders", "orders"
                            ),
                            ft.Container(height=20),
                            atoms.caption_text("SETTINGS", color=ft.Colors.GREY_500),
                            ft.Container(height=10),
                            create_menu_item(ft.Icons.SETTINGS, "Settings", "settings"),
                            create_menu_item(ft.Icons.HELP, "Help", "help"),
                        ],
                        spacing=5,
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=20),
                    expand=True,
                ),
                # User section
                atoms.horizontal_divider(color=ft.Colors.BLUE_800),
                ft.Container(
                    content=ft.Row(
                        [
                            molecules.user_avatar("Admin User"),
                            ft.Column(
                                [
                                    atoms.body_text(
                                        "Admin User",
                                        color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    atoms.caption_text(
                                        "admin@example.com", color=ft.Colors.GREY_400
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                ),
            ],
            spacing=0,
        ),
        width=280,
        bgcolor=ft.Colors.BLUE_900,
        border_radius=ft.border_radius.only(top_right=12, bottom_right=12),
    )


# ============================================================================
# TOP BAR ORGANISM
# ============================================================================


def top_bar(title: str, search_ref: ft.Ref = None) -> ft.Container:
    """
    Top bar organism: Page header with title and search.

    Composed of:
    - Heading1 atom (title)
    - Search bar molecule
    - Icon button atoms (notifications, etc.)
    """
    return ft.Container(
        content=ft.Row(
            [
                atoms.heading1(title),
                ft.Container(expand=True),
                molecules.search_bar(ref=search_ref),
                atoms.icon_button(
                    ft.Icons.NOTIFICATIONS,
                    tooltip="Notifications",
                ),
                atoms.icon_button(
                    ft.Icons.SETTINGS,
                    tooltip="Settings",
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_200)),
    )


# ============================================================================
# STATS GRID ORGANISM
# ============================================================================


def stats_grid(
    total_users_ref: ft.Ref = None,
    revenue_ref: ft.Ref = None,
    orders_ref: ft.Ref = None,
    growth_ref: ft.Ref = None,
) -> ft.Container:
    """
    Stats grid organism: Dashboard metrics overview.

    Composed of:
    - 4 stat card molecules arranged in a grid
    """
    return ft.Container(
        content=ft.ResponsiveRow(
            [
                ft.Container(
                    molecules.stat_card(
                        "Total Users",
                        "0",
                        ft.Icons.PEOPLE,
                        ft.Colors.BLUE_700,
                        ref=total_users_ref,
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    molecules.stat_card(
                        "Revenue",
                        "$0",
                        ft.Icons.ATTACH_MONEY,
                        ft.Colors.GREEN_700,
                        ref=revenue_ref,
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    molecules.stat_card(
                        "Orders",
                        "0",
                        ft.Icons.SHOPPING_CART,
                        ft.Colors.ORANGE_700,
                        ref=orders_ref,
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    molecules.stat_card(
                        "Growth",
                        "0%",
                        ft.Icons.TRENDING_UP,
                        ft.Colors.PURPLE_700,
                        ref=growth_ref,
                    ),
                    col={"sm": 12, "md": 6, "lg": 3},
                ),
            ],
            spacing=20,
        ),
        padding=30,
    )


# ============================================================================
# DATA TABLE ORGANISM
# ============================================================================


def data_table(title: str, headers: list, rows: list = None) -> ft.Container:
    """
    Data table organism: Complete table with headers and rows.

    Composed of:
    - Heading3 atom (title)
    - Data row molecules (headers)
    - Multiple data row molecules (data)
    - Card container atom
    """
    rows = rows or []

    return atoms.card_container(
        content=ft.Column(
            [
                # Table header
                ft.Row(
                    [
                        atoms.heading3(title),
                        ft.Container(expand=True),
                        atoms.secondary_button("Export", icon=ft.Icons.DOWNLOAD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                atoms.horizontal_divider(),
                # Column headers
                ft.Container(
                    content=ft.Row(
                        [
                            atoms.body_text(h, weight=ft.FontWeight.BOLD, expand=True)
                            for h in headers
                        ],
                        spacing=10,
                    ),
                    padding=15,
                    bgcolor=ft.Colors.GREY_50,
                ),
                # Data rows
                ft.Column(
                    [molecules.data_row(row) for row in rows]
                    if rows
                    else [
                        ft.Container(
                            content=atoms.body_text(
                                "No data available", color=ft.Colors.GREY_500
                            ),
                            padding=30,
                            alignment=ft.alignment.center,
                        )
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=15,
        ),
    )


# ============================================================================
# SETTINGS FORM ORGANISM
# ============================================================================


def settings_form(
    name_ref: ft.Ref = None, email_ref: ft.Ref = None, on_save=None
) -> ft.Container:
    """
    Settings form organism: User settings form.

    Composed of:
    - Heading3 atom (title)
    - Multiple form field molecules
    - Primary button atom
    - Card container atom
    """
    return atoms.card_container(
        content=ft.Column(
            [
                atoms.heading3("Profile Settings"),
                atoms.horizontal_divider(),
                molecules.form_field("Full Name", required=True, ref=name_ref),
                molecules.form_field("Email Address", required=True, ref=email_ref),
                molecules.form_field("Phone Number", hint="+1 (555) 000-0000"),
                ft.Container(height=10),
                ft.Row(
                    [
                        atoms.primary_button("Save Changes", on_click=on_save),
                        atoms.secondary_button("Cancel"),
                    ],
                    spacing=10,
                ),
            ],
            spacing=20,
        ),
    )
