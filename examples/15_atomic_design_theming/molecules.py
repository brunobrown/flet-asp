"""
Theme-Aware Molecules: Component combinations that adapt to themes

These molecules combine theme-aware atoms into functional units
that automatically respond to theme changes.
"""

import flet as ft
import atoms
from theme_tokens import get_theme


# ============================================================================
# ALERT MOLECULE
# ============================================================================


def alert(
    message: str, severity: str = "info", dismissible: bool = False, on_dismiss=None
) -> ft.Container:
    """
    Alert molecule: Colored notification banner.

    Severity: "success", "warning", "error", "info"
    """
    theme = get_theme()

    icon_map = {
        "success": (ft.Icons.CHECK_CIRCLE, theme.colors.success),
        "warning": (ft.Icons.WARNING, theme.colors.warning),
        "error": (ft.Icons.ERROR, theme.colors.error),
        "info": (ft.Icons.INFO, theme.colors.info),
    }

    icon_name, icon_color = icon_map.get(severity, icon_map["info"])

    content_row = ft.Row(
        [
            atoms.icon(icon_name, semantic=severity),
            atoms.body_text(message, expand=True),
        ],
        spacing=theme.spacing.sm,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    if dismissible:
        content_row.controls.append(
            atoms.icon_button(
                ft.Icons.CLOSE,
                on_click=on_dismiss,
            )
        )

    return ft.Container(
        content=content_row,
        padding=theme.spacing.md,
        border_radius=theme.radius.md,
        bgcolor=ft.Colors.with_opacity(0.1, icon_color),
        border=ft.border.all(1, icon_color),
    )


# ============================================================================
# INPUT GROUP MOLECULE
# ============================================================================


def input_group(
    label: str, help_text: str = None, error: str = None, ref: ft.Ref = None, **kwargs
) -> ft.Column:
    """
    Input group molecule: Label + input + help/error text.
    """
    theme = get_theme()

    controls = [atoms.body_text(label, weight=ft.FontWeight.W_500)]

    controls.append(atoms.text_field(ref=ref, **kwargs))

    if error:
        controls.append(atoms.label_text(error, color=theme.colors.error))
    elif help_text:
        controls.append(atoms.label_text(help_text, color=theme.colors.text_secondary))

    return ft.Column(
        controls,
        spacing=theme.spacing.xs,
    )


# ============================================================================
# STAT CARD MOLECULE
# ============================================================================


def stat_card(
    label: str,
    value: str,
    icon_name: str = None,
    trend: str = None,
    trend_positive: bool = True,
    ref: ft.Ref = None,
) -> ft.Container:
    """
    Stat card molecule: Displays a metric with optional trend.

    Args:
        label: Metric name
        value: Metric value
        icon_name: Optional icon
        trend: Optional trend text (e.g., "+12.5%")
        trend_positive: Whether trend is positive (green) or negative (red)
    """
    theme = get_theme()

    controls = []

    # Icon and value row
    value_row = ft.Row(
        spacing=theme.spacing.md,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    if icon_name:
        value_row.controls.append(
            ft.Container(
                content=atoms.icon(icon_name, size=32, semantic="primary"),
                width=56,
                height=56,
                border_radius=theme.radius.full,
                bgcolor=ft.Colors.with_opacity(0.1, theme.colors.primary),
                alignment=ft.alignment.center,
            )
        )

    value_col = ft.Column(
        [
            atoms.label_text(label),
            atoms.headline_text(value, level=2, ref=ref)
            if ref
            else atoms.headline_text(value, level=2),
        ],
        spacing=theme.spacing.xs,
        expand=True,
    )

    value_row.controls.append(value_col)
    controls.append(value_row)

    # Trend indicator
    if trend:
        trend_color = theme.colors.success if trend_positive else theme.colors.error
        trend_icon = (
            ft.Icons.ARROW_UPWARD if trend_positive else ft.Icons.ARROW_DOWNWARD
        )

        controls.append(
            ft.Row(
                [
                    ft.Icon(trend_icon, size=16, color=trend_color),
                    atoms.label_text(trend, color=trend_color),
                ],
                spacing=theme.spacing.xs,
            )
        )

    return atoms.surface(
        content=ft.Column(
            controls,
            spacing=theme.spacing.sm,
        ),
    )


# ============================================================================
# LIST ITEM MOLECULE
# ============================================================================


def list_item(
    title: str,
    subtitle: str = None,
    leading_icon: str = None,
    trailing: ft.Control = None,
    on_click=None,
) -> ft.Container:
    """
    List item molecule: Title + subtitle with optional icons/actions.
    """
    theme = get_theme()

    controls = []

    if leading_icon:
        controls.append(atoms.icon(leading_icon))

    text_col = ft.Column(
        [atoms.body_text(title, weight=ft.FontWeight.W_500)],
        spacing=theme.spacing.xs,
        expand=True,
    )

    if subtitle:
        text_col.controls.append(atoms.label_text(subtitle))

    controls.append(text_col)

    if trailing:
        controls.append(trailing)

    return ft.Container(
        content=ft.Row(
            controls,
            spacing=theme.spacing.md,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=theme.spacing.md,
        border_radius=theme.radius.md,
        on_click=on_click,
        ink=True if on_click else False,
        border=ft.border.only(bottom=ft.BorderSide(1, theme.colors.divider)),
    )


# ============================================================================
# AVATAR MOLECULE
# ============================================================================


def avatar(name: str, size: int = 40, on_click=None) -> ft.Container:
    """
    Avatar molecule: Shows user initials in a circle.
    """
    theme = get_theme()
    initials = "".join([word[0].upper() for word in name.split()[:2]])

    return ft.Container(
        content=ft.Text(
            initials,
            size=size // 2.5,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
        width=size,
        height=size,
        border_radius=size // 2,
        bgcolor=theme.colors.primary,
        alignment=ft.alignment.center,
        on_click=on_click,
        ink=True if on_click else False,
    )


# ============================================================================
# BADGE MOLECULE
# ============================================================================


def badge(text: str, semantic: str = None) -> ft.Container:
    """
    Badge molecule: Colored label tag.

    Semantic: "success", "warning", "error", "info", None (default)
    """
    theme = get_theme()

    color_map = {
        "success": theme.colors.success,
        "warning": theme.colors.warning,
        "error": theme.colors.error,
        "info": theme.colors.info,
    }

    bg_color = color_map.get(semantic, theme.colors.primary)

    return ft.Container(
        content=atoms.label_text(
            text, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
        ),
        padding=ft.padding.symmetric(
            horizontal=theme.spacing.sm,
            vertical=theme.spacing.xs,
        ),
        border_radius=theme.radius.full,
        bgcolor=bg_color,
    )


# ============================================================================
# THEME TOGGLE MOLECULE
# ============================================================================


def theme_toggle(current_mode: str, on_toggle) -> ft.Container:
    """
    Theme toggle molecule: Switch between light/dark mode.

    Args:
        current_mode: "light" or "dark"
        on_toggle: Callback when toggled
    """
    theme = get_theme()

    is_dark = current_mode == "dark"

    return ft.Container(
        content=ft.Row(
            [
                atoms.icon(
                    ft.Icons.LIGHT_MODE if not is_dark else ft.Icons.DARK_MODE,
                    semantic="primary",
                ),
                atoms.body_text(
                    "Dark Mode" if is_dark else "Light Mode",
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(expand=True),
                atoms.switch(value=is_dark, on_change=on_toggle),
            ],
            spacing=theme.spacing.sm,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=theme.spacing.md,
        border_radius=theme.radius.md,
        bgcolor=theme.colors.surface_variant,
    )
