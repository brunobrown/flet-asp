"""
Templates: Page-level layouts that position organisms and reveal content structure.

Templates establish the page skeleton and layout patterns, showing where
organisms will be placed without specifying final content.
"""

import flet as ft

# Handle both direct execution and module import
try:
    from . import organisms
except ImportError:
    import organisms


# ============================================================================
# DASHBOARD TEMPLATE
# ============================================================================


def dashboard_template(
    page: ft.Page,
    current_view: str,
    title: str,
    content: ft.Control,
    search_ref: ft.Ref = None,
) -> ft.Row:
    """
    Dashboard template: Standard layout with sidebar and main content.

    Layout structure:
    +----------------+--------------------------------+
    |                |     Top Bar                    |
    |   Sidebar      +--------------------------------+
    |                |                                |
    |                |     Main Content               |
    |                |                                |
    +----------------+--------------------------------+

    Composed of:
    - Sidebar organism
    - Top bar organism
    - Content area (accepts any organism/page)
    """
    return ft.Row(
        [
            # Left sidebar
            organisms.sidebar(page, current_view),
            # Main content area
            ft.Column(
                [
                    organisms.top_bar(title, search_ref),
                    ft.Container(
                        content=content,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )


# ============================================================================
# CENTERED CONTENT TEMPLATE
# ============================================================================


def centered_content_template(
    page: ft.Page,
    current_view: str,
    title: str,
    content: ft.Control,
    max_width: int = 800,
) -> ft.Row:
    """
    Centered content template: Layout with centered, constrained content.

    Good for forms, settings pages, or focused content.

    Layout structure:
    +----------------+--------------------------------+
    |                |     Top Bar                    |
    |   Sidebar      +--------------------------------+
    |                |                                |
    |                |   +--------------------+       |
    |                |   |  Centered Content  |       |
    |                |   +--------------------+       |
    |                |                                |
    +----------------+--------------------------------+

    Composed of:
    - Sidebar organism
    - Top bar organism
    - Centered content container
    """
    return ft.Row(
        [
            # Left sidebar
            organisms.sidebar(page, current_view),
            # Main content area
            ft.Column(
                [
                    organisms.top_bar(title),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=content,
                                    width=max_width,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=30,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )


# ============================================================================
# FULL WIDTH CONTENT TEMPLATE
# ============================================================================


def full_width_template(
    page: ft.Page, current_view: str, title: str, content: ft.Control
) -> ft.Row:
    """
    Full width template: Layout with full-width content area.

    Good for tables, charts, or data-heavy pages.

    Layout structure:
    +----------------+--------------------------------+
    |                |     Top Bar                    |
    |   Sidebar      +--------------------------------+
    |                |                                |
    |                |   Full Width Content           |
    |                |                                |
    +----------------+--------------------------------+

    Composed of:
    - Sidebar organism
    - Top bar organism
    - Full-width content area
    """
    return ft.Row(
        [
            # Left sidebar
            organisms.sidebar(page, current_view),
            # Main content area
            ft.Column(
                [
                    organisms.top_bar(title),
                    ft.Container(
                        content=content,
                        padding=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
