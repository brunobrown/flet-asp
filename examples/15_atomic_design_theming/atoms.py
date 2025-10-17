"""
Theme-Aware Atoms: Basic UI elements that adapt to theme changes

These atoms use theme tokens instead of hardcoded colors,
making them automatically responsive to theme switching.
"""

import flet as ft

# Handle both direct execution and module import
try:
    from .theme_tokens import get_theme
except ImportError:
    from theme_tokens import get_theme


# ============================================================================
# TEXT ATOMS
# ============================================================================


def display_text(text: str, color: str = None, **kwargs) -> ft.Text:
    """Large display text atom."""
    theme = get_theme()
    return ft.Text(
        text,
        size=theme.typography.display_small,
        weight=ft.FontWeight.BOLD,
        color=color or theme.colors.text_primary,
        **kwargs,
    )


def headline_text(text: str, level: int = 1, color: str = None, **kwargs) -> ft.Text:
    """Headline text atom (levels 1-3)."""
    theme = get_theme()
    sizes = [
        theme.typography.headline_large,
        theme.typography.headline_medium,
        theme.typography.headline_small,
    ]
    return ft.Text(
        text,
        size=sizes[level - 1],
        weight=ft.FontWeight.BOLD,
        color=color or theme.colors.text_primary,
        **kwargs,
    )


def title_text(text: str, level: int = 1, color: str = None, **kwargs) -> ft.Text:
    """Title text atom (levels 1-3)."""
    theme = get_theme()
    sizes = [
        theme.typography.title_large,
        theme.typography.title_medium,
        theme.typography.title_small,
    ]
    return ft.Text(
        text,
        size=sizes[level - 1],
        weight=ft.FontWeight.W_600,
        color=color or theme.colors.text_primary,
        **kwargs,
    )


def body_text(
    text: str, secondary: bool = False, color: str = None, **kwargs
) -> ft.Text:
    """Body text atom."""
    theme = get_theme()
    return ft.Text(
        text,
        size=theme.typography.body_medium,
        color=color
        or (theme.colors.text_secondary if secondary else theme.colors.text_primary),
        **kwargs,
    )


def label_text(text: str, color: str = None, **kwargs) -> ft.Text:
    """Small label text atom."""
    theme = get_theme()
    return ft.Text(
        text,
        size=theme.typography.label_small,
        color=color or theme.colors.text_secondary,
        **kwargs,
    )


# ============================================================================
# BUTTON ATOMS
# ============================================================================


def filled_button(
    text: str, on_click=None, icon: str = None, **kwargs
) -> ft.ElevatedButton:
    """Filled (primary) button atom."""
    theme = get_theme()
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=theme.colors.primary,
        ),
        **kwargs,
    )


def outlined_button(
    text: str, on_click=None, icon: str = None, **kwargs
) -> ft.OutlinedButton:
    """Outlined button atom."""
    theme = get_theme()
    return ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=theme.colors.primary,
            side=ft.BorderSide(2, theme.colors.primary),
        ),
        **kwargs,
    )


def text_button(text: str, on_click=None, icon: str = None, **kwargs) -> ft.TextButton:
    """Text button atom."""
    theme = get_theme()
    return ft.TextButton(
        text=text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=theme.colors.primary,
        ),
        **kwargs,
    )


def icon_button(
    icon: str, on_click=None, tooltip: str = None, **kwargs
) -> ft.IconButton:
    """Icon button atom."""
    theme = get_theme()
    return ft.IconButton(
        icon=icon,
        on_click=on_click,
        tooltip=tooltip,
        icon_color=theme.colors.primary,
        **kwargs,
    )


# ============================================================================
# INPUT ATOMS
# ============================================================================


def text_field(label: str = None, hint: str = None, **kwargs) -> ft.TextField:
    """Text input field atom."""
    theme = get_theme()
    return ft.TextField(
        label=label,
        hint_text=hint,
        border_color=theme.colors.border,
        focused_border_color=theme.colors.primary,
        bgcolor=theme.colors.surface,
        color=theme.colors.text_primary,
        **kwargs,
    )


def dropdown_field(label: str = None, options: list = None, **kwargs) -> ft.Dropdown:
    """Dropdown field atom."""
    theme = get_theme()
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(opt) for opt in (options or [])],
        border_color=theme.colors.border,
        focused_border_color=theme.colors.primary,
        bgcolor=theme.colors.surface,
        color=theme.colors.text_primary,
        **kwargs,
    )


def checkbox(label: str = None, **kwargs) -> ft.Checkbox:
    """Checkbox atom."""
    theme = get_theme()
    return ft.Checkbox(label=label, fill_color=theme.colors.primary, **kwargs)


def switch(label: str = None, **kwargs) -> ft.Switch:
    """Switch atom."""
    theme = get_theme()
    return ft.Switch(label=label, active_color=theme.colors.primary, **kwargs)


# ============================================================================
# ICON ATOMS
# ============================================================================


def icon(name: str, size: int = 24, semantic: str = None) -> ft.Icon:
    """Icon atom with optional semantic coloring."""
    theme = get_theme()

    color_map = {
        "success": theme.colors.success,
        "warning": theme.colors.warning,
        "error": theme.colors.error,
        "info": theme.colors.info,
        "primary": theme.colors.primary,
    }

    return ft.Icon(
        name=name,
        size=size,
        color=color_map.get(semantic, theme.colors.text_secondary),
    )


# ============================================================================
# DIVIDER ATOMS
# ============================================================================


def divider(**kwargs) -> ft.Divider:
    """Horizontal divider atom."""
    theme = get_theme()
    return ft.Divider(height=1, color=theme.colors.divider, **kwargs)


def vertical_divider(**kwargs) -> ft.VerticalDivider:
    """Vertical divider atom."""
    theme = get_theme()
    return ft.VerticalDivider(width=1, color=theme.colors.divider, **kwargs)


# ============================================================================
# CONTAINER ATOMS
# ============================================================================


def card(content, **kwargs) -> ft.Container:
    """Card container atom."""
    theme = get_theme()
    return ft.Container(
        content=content,
        padding=theme.spacing.lg,
        border_radius=theme.radius.lg,
        bgcolor=theme.colors.surface,
        border=ft.border.all(1, theme.colors.border),
        **kwargs,
    )


def surface(content, **kwargs) -> ft.Container:
    """Surface container atom (elevated card)."""
    theme = get_theme()
    return ft.Container(
        content=content,
        padding=theme.spacing.lg,
        border_radius=theme.radius.lg,
        bgcolor=theme.colors.surface,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        **kwargs,
    )


def chip(text: str, on_delete=None, **kwargs) -> ft.Container:
    """Chip atom (small labeled tag)."""
    theme = get_theme()

    content = ft.Row(
        [
            label_text(text, color=theme.colors.text_primary),
        ],
        spacing=theme.spacing.xs,
        tight=True,
    )

    if on_delete:
        content.controls.append(
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_size=14,
                on_click=on_delete,
            )
        )

    return ft.Container(
        content=content,
        padding=ft.padding.symmetric(
            horizontal=theme.spacing.sm,
            vertical=theme.spacing.xs,
        ),
        border_radius=theme.radius.full,
        bgcolor=theme.colors.surface_variant,
        border=ft.border.all(1, theme.colors.border),
        **kwargs,
    )
