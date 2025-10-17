"""
Theme Tokens: Design system foundation

Theme tokens are the most atomic level of a design system - they define
the visual language (colors, typography, spacing) that all components use.

This module provides a reactive theme system where tokens automatically
update when the theme mode changes.
"""

import flet as ft
from dataclasses import dataclass
from typing import Literal


ThemeMode = Literal["light", "dark"]


# ============================================================================
# COLOR TOKENS
# ============================================================================


@dataclass
class ColorTokens:
    """Color palette for a theme."""

    # Primary colors
    primary: str
    primary_dark: str
    primary_light: str

    # Neutral colors
    background: str
    surface: str
    surface_variant: str

    # Text colors
    text_primary: str
    text_secondary: str
    text_disabled: str

    # Semantic colors
    success: str
    warning: str
    error: str
    info: str

    # Border colors
    border: str
    border_light: str
    divider: str


# Light theme colors
LIGHT_COLORS = ColorTokens(
    primary=ft.Colors.BLUE_700,
    primary_dark=ft.Colors.BLUE_900,
    primary_light=ft.Colors.BLUE_500,
    background=ft.Colors.GREY_50,
    surface=ft.Colors.WHITE,
    surface_variant=ft.Colors.GREY_100,
    text_primary=ft.Colors.GREY_900,
    text_secondary=ft.Colors.GREY_700,
    text_disabled=ft.Colors.GREY_400,
    success=ft.Colors.GREEN_600,
    warning=ft.Colors.ORANGE_600,
    error=ft.Colors.RED_600,
    info=ft.Colors.BLUE_600,
    border=ft.Colors.GREY_300,
    border_light=ft.Colors.GREY_200,
    divider=ft.Colors.GREY_200,
)


# Dark theme colors
DARK_COLORS = ColorTokens(
    primary=ft.Colors.BLUE_400,
    primary_dark=ft.Colors.BLUE_600,
    primary_light=ft.Colors.BLUE_300,
    background=ft.Colors.GREY_900,
    surface=ft.Colors.GREY_800,
    surface_variant=ft.Colors.GREY_700,
    text_primary=ft.Colors.GREY_100,
    text_secondary=ft.Colors.GREY_400,
    text_disabled=ft.Colors.GREY_600,
    success=ft.Colors.GREEN_400,
    warning=ft.Colors.ORANGE_400,
    error=ft.Colors.RED_400,
    info=ft.Colors.BLUE_400,
    border=ft.Colors.GREY_700,
    border_light=ft.Colors.GREY_600,
    divider=ft.Colors.GREY_700,
)


# ============================================================================
# TYPOGRAPHY TOKENS
# ============================================================================


@dataclass
class TypographyTokens:
    """Typography scale for consistent text styling."""

    # Display
    display_large: int = 57
    display_medium: int = 45
    display_small: int = 36

    # Headline
    headline_large: int = 32
    headline_medium: int = 28
    headline_small: int = 24

    # Title
    title_large: int = 22
    title_medium: int = 16
    title_small: int = 14

    # Body
    body_large: int = 16
    body_medium: int = 14
    body_small: int = 12

    # Label
    label_large: int = 14
    label_medium: int = 12
    label_small: int = 11


TYPOGRAPHY = TypographyTokens()


# ============================================================================
# SPACING TOKENS
# ============================================================================


@dataclass
class SpacingTokens:
    """Spacing scale for consistent layouts."""

    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    xxxl: int = 64


SPACING = SpacingTokens()


# ============================================================================
# RADIUS TOKENS
# ============================================================================


@dataclass
class RadiusTokens:
    """Border radius scale."""

    none: int = 0
    sm: int = 4
    md: int = 8
    lg: int = 12
    xl: int = 16
    full: int = 999


RADIUS = RadiusTokens()


# ============================================================================
# THEME MANAGER
# ============================================================================


class ThemeManager:
    """Manages current theme and provides token access."""

    def __init__(self, mode: ThemeMode = "light"):
        self._mode: ThemeMode = mode
        self._observers = []

    @property
    def mode(self) -> ThemeMode:
        """Current theme mode."""
        return self._mode

    @mode.setter
    def mode(self, value: ThemeMode):
        """Set theme mode and notify observers."""
        if value != self._mode:
            self._mode = value
            self._notify_observers()

    @property
    def colors(self) -> ColorTokens:
        """Get current color tokens."""
        return DARK_COLORS if self._mode == "dark" else LIGHT_COLORS

    @property
    def typography(self) -> TypographyTokens:
        """Get typography tokens."""
        return TYPOGRAPHY

    @property
    def spacing(self) -> SpacingTokens:
        """Get spacing tokens."""
        return SPACING

    @property
    def radius(self) -> RadiusTokens:
        """Get radius tokens."""
        return RADIUS

    def observe(self, callback):
        """Register observer for theme changes."""
        self._observers.append(callback)

    def _notify_observers(self):
        """Notify all observers of theme change."""
        for callback in self._observers:
            callback(self._mode)

    def toggle(self):
        """Toggle between light and dark mode."""
        self.mode = "dark" if self._mode == "light" else "light"


# Global theme manager instance
_theme_manager = None


def get_theme() -> ThemeManager:
    """Get global theme manager instance."""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
