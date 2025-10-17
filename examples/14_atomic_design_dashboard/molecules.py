"""
Molecules: Simple combinations of atoms that work together as a unit.

Molecules do one thing well and are the building blocks for more
complex organisms. Each molecule combines 2-5 atoms into a functional unit.
"""

import flet as ft

# Handle both direct execution and module import
try:
    from . import atoms
except ImportError:
    import atoms


# ============================================================================
# STAT CARD MOLECULE
# ============================================================================


def stat_card(
    title: str, value: str, icon_name: str, color: str = None, ref: ft.Ref = None
) -> ft.Container:
    """
    Stat card molecule: Shows a metric with title, value, and icon.

    Composed of:
    - Icon atom
    - Heading3 atom (title)
    - Heading2 atom (value)
    - Card container atom
    """
    return atoms.card_container(
        content=ft.Row(
            [
                ft.Container(
                    content=atoms.icon(
                        icon_name, size=32, color=color or ft.Colors.BLUE_700
                    ),
                    width=60,
                    height=60,
                    border_radius=30,
                    bgcolor=ft.Colors.BLUE_50,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        atoms.caption_text(title),
                        atoms.heading2(value, ref=ref)
                        if ref
                        else atoms.heading2(value),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
        ),
        ref=ref if not ref else None,
    )


# ============================================================================
# MENU ITEM MOLECULE
# ============================================================================


def menu_item(
    icon_name: str, label: str, on_click=None, selected: bool = False
) -> ft.Container:
    """
    Menu item molecule: Sidebar navigation item.

    Composed of:
    - Icon atom
    - Body text atom
    - Container atom (for hover/selected states)
    """
    return ft.Container(
        content=ft.Row(
            [
                atoms.icon(
                    icon_name,
                    size=20,
                    color=ft.Colors.WHITE if selected else ft.Colors.GREY_400,
                ),
                atoms.body_text(
                    label,
                    color=ft.Colors.WHITE if selected else ft.Colors.GREY_400,
                    weight=ft.FontWeight.W_600 if selected else ft.FontWeight.NORMAL,
                ),
            ],
            spacing=15,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        bgcolor=ft.Colors.BLUE_800 if selected else ft.Colors.TRANSPARENT,
        border_radius=8,
        on_click=on_click,
        ink=True,
    )


# ============================================================================
# FORM FIELD MOLECULE
# ============================================================================


def form_field(
    label: str, required: bool = False, ref: ft.Ref = None, **kwargs
) -> ft.Column:
    """
    Form field molecule: Label + input with validation indicator.

    Composed of:
    - Body text atom (label)
    - Text input atom
    """
    label_text = f"{label} *" if required else label

    return ft.Column(
        [
            atoms.body_text(label_text, weight=ft.FontWeight.W_500),
            atoms.text_input(ref=ref, **kwargs),
        ],
        spacing=8,
    )


# ============================================================================
# SEARCH BAR MOLECULE
# ============================================================================


def search_bar(
    hint: str = "Search...", on_change=None, ref: ft.Ref = None
) -> ft.Container:
    """
    Search bar molecule: Search icon + input field.

    Composed of:
    - Icon atom
    - Text input atom
    - Container atom
    """
    return ft.Container(
        content=ft.Row(
            [
                atoms.icon(ft.Icons.SEARCH, size=20),
                ft.TextField(
                    hint_text=hint,
                    border=ft.InputBorder.NONE,
                    text_size=14,
                    on_change=on_change,
                    ref=ref,
                    expand=True,
                ),
            ],
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=15, vertical=5),
        border_radius=25,
        bgcolor=ft.Colors.GREY_100,
        border=ft.border.all(1, ft.Colors.GREY_300),
    )


# ============================================================================
# USER AVATAR MOLECULE
# ============================================================================


def user_avatar(name: str, on_click=None) -> ft.Container:
    """
    User avatar molecule: Shows user initials or icon.

    Composed of:
    - Text atom (initials)
    - Container atom (circular)
    """
    initials = "".join([word[0].upper() for word in name.split()[:2]])

    return ft.Container(
        content=atoms.body_text(
            initials,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        ),
        width=40,
        height=40,
        border_radius=20,
        bgcolor=ft.Colors.BLUE_700,
        alignment=ft.alignment.center,
        on_click=on_click,
        ink=True,
    )


# ============================================================================
# BADGE MOLECULE
# ============================================================================


def badge(text: str, color: str = None) -> ft.Container:
    """
    Badge molecule: Small labeled tag.

    Composed of:
    - Caption text atom
    - Container atom
    """
    return ft.Container(
        content=atoms.caption_text(
            text,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        ),
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
        border_radius=12,
        bgcolor=color or ft.Colors.BLUE_700,
    )


# ============================================================================
# DATA ROW MOLECULE
# ============================================================================


def data_row(columns: list, on_click=None) -> ft.Container:
    """
    Data row molecule: Row of data in a table.

    Composed of:
    - Multiple body text atoms
    - Container atom (for hover effect)
    """
    return ft.Container(
        content=ft.Row(
            [atoms.body_text(str(col), expand=True) for col in columns],
            spacing=10,
        ),
        padding=15,
        border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_200)),
        on_click=on_click,
        ink=True,
    )
