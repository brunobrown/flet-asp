"""
Atoms: Basic UI elements that cannot be broken down further.

These are the foundational building blocks of our design system.
Each atom is a single, reusable UI element with consistent styling.
"""

import flet as ft


# ============================================================================
# TEXT ATOMS
# ============================================================================


def heading1(text: str, color: str = None, **kwargs) -> ft.Text:
    """H1 heading atom."""
    return ft.Text(text, size=32, weight=ft.FontWeight.BOLD, color=color, **kwargs)


def heading2(text: str, color: str = None, **kwargs) -> ft.Text:
    """H2 heading atom."""
    return ft.Text(text, size=24, weight=ft.FontWeight.BOLD, color=color, **kwargs)


def heading3(text: str, color: str = None, **kwargs) -> ft.Text:
    """H3 heading atom."""
    return ft.Text(text, size=18, weight=ft.FontWeight.W_600, color=color, **kwargs)


def body_text(text: str, color: str = None, **kwargs) -> ft.Text:
    """Body text atom."""
    return ft.Text(text, size=14, color=color, **kwargs)


def caption_text(text: str, color: str = None, **kwargs) -> ft.Text:
    """Caption text atom (small, muted)."""
    return ft.Text(text, size=12, color=color or ft.Colors.GREY_600, **kwargs)


# ============================================================================
# BUTTON ATOMS
# ============================================================================


def primary_button(text: str, on_click=None, **kwargs) -> ft.ElevatedButton:
    """Primary action button atom."""
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
        ),
        **kwargs,
    )


def secondary_button(text: str, on_click=None, **kwargs) -> ft.OutlinedButton:
    """Secondary action button atom."""
    return ft.OutlinedButton(
        text=text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE_700,
        ),
        **kwargs,
    )


def icon_button(
    icon: str, on_click=None, tooltip: str = None, **kwargs
) -> ft.IconButton:
    """Icon button atom."""
    return ft.IconButton(icon=icon, on_click=on_click, tooltip=tooltip, **kwargs)


# ============================================================================
# INPUT ATOMS
# ============================================================================


def text_input(label: str = None, hint: str = None, **kwargs) -> ft.TextField:
    """Text input field atom."""
    return ft.TextField(
        label=label,
        hint_text=hint,
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.BLUE_900,
        **kwargs,
    )


def dropdown(label: str = None, options: list = None, **kwargs) -> ft.Dropdown:
    """Dropdown select atom."""
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(opt) for opt in (options or [])],
        border_color=ft.Colors.BLUE_700,
        focused_border_color=ft.Colors.BLUE_900,
        **kwargs,
    )


# ============================================================================
# ICON ATOMS
# ============================================================================


def icon(name: str, size: int = 24, color: str = None) -> ft.Icon:
    """Icon atom."""
    return ft.Icon(
        name=name,
        size=size,
        color=color or ft.Colors.GREY_700,
    )


# ============================================================================
# DIVIDER ATOMS
# ============================================================================


def horizontal_divider(color: str = None, **kwargs) -> ft.Divider:
    """Horizontal divider atom."""
    return ft.Divider(height=1, color=color or ft.Colors.GREY_300, **kwargs)


def vertical_divider(color: str = None, **kwargs) -> ft.VerticalDivider:
    """Vertical divider atom."""
    return ft.VerticalDivider(width=1, color=color or ft.Colors.GREY_300, **kwargs)


# ============================================================================
# CONTAINER ATOMS
# ============================================================================


def card_container(content, **kwargs) -> ft.Container:
    """Card-style container atom."""
    return ft.Container(
        content=content,
        padding=20,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        **kwargs,
    )
