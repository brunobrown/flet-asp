"""
Atoms - Basic UI components that cannot be decomposed.
Following the Atomic Design pattern with Flet-ASP.
"""

import flet as ft


def send_icon(
    ref: ft.Ref = None,
    size: int = 16,
    color: str = ft.Colors.WHITE,
    initial_rotation: float = 11,
) -> ft.IconButton:
    """
    Atom: Send icon (airplane) with animation settings.
    """
    return ft.IconButton(
        ref=ref,
        icon=ft.Icons.SEND_SHARP,
        icon_color=color,
        icon_size=size,
        offset=ft.Offset(0, 0),
        animate_offset=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),
        rotate=ft.Rotate(initial_rotation, alignment=ft.alignment.center),
        animate_rotation=ft.Animation(duration=600, curve=ft.AnimationCurve.DECELERATE),
        scale=ft.Scale(1),
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_OUT),
    )


def button_text(
    ref: ft.Ref = None,
    value: str = "SEND",
    size: int = 14,
    color: str = ft.Colors.WHITE,
    weight: ft.FontWeight = ft.FontWeight.W_700,
) -> ft.Text:
    """
    Atom: Button text with animation settings.
    """
    return ft.Text(
        ref=ref,
        value=value,
        color=color,
        size=size,
        weight=weight,
        opacity=1,
        offset=ft.Offset(0, 0),
        animate_offset=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT),
        animate_opacity=ft.Animation(duration=200),
    )


def cloud_icon(
    ref: ft.Ref = None,
    size: int = 12,
    color: str = ft.Colors.WHITE54,
    top: int = None,
    bottom: int = None,
    animation_duration: int = 1200,
) -> ft.Container:
    """
    Atom: Cloud icon for parallax effect.
    """
    return ft.Container(
        ref=ref,
        content=ft.Icon(ft.Icons.CLOUD, color=color, size=size),
        left=130,
        top=top,
        bottom=bottom,
        animate_position=ft.Animation(
            duration=animation_duration, curve=ft.AnimationCurve.LINEAR
        ),
        opacity=0,
    )


def button_container(
    width: int = 130,
    height: int = 45,
    bgcolor: str = ft.Colors.BLUE_700,
    border_radius: int = 10,
    content: ft.Control = None,
    on_hover=None,
    on_click=None,
) -> ft.Container:
    """
    Atom: Base button container with clipping for parallax.
    """
    return ft.Container(
        width=width,
        height=height,
        bgcolor=bgcolor,
        border_radius=border_radius,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        on_hover=on_hover,
        on_click=on_click,
        content=content,
    )


def loading_bar(
    ref: ft.Ref = None,
    progress_ref: ft.Ref = None,
    width: int = 130,
    height: int = 6,
    bgcolor: str = ft.Colors.BLUE_300,
    bar_color: str = ft.Colors.WHITE,
) -> ft.Container:
    """
    Atom: Loading bar with progress animation using native ProgressBar.
    """
    return ft.Container(
        ref=ref,
        width=width,
        height=height,
        opacity=0,
        animate_opacity=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE_IN_OUT),
        content=ft.ProgressBar(
            ref=progress_ref,  # Ref for the ProgressBar
            value=0,
            width=width,
            height=height,
            bgcolor=bgcolor,
            color=bar_color,
            border_radius=3,
        ),
    )
