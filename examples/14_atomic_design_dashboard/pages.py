"""
Pages: Specific instances of templates with real content.

Pages are complete screens that use templates and populate them with
actual data and state bindings. This is where flet-asp state management
connects to the design system.
"""

import flet as ft

# Handle both direct execution and module import
try:
    from . import templates, organisms
except ImportError:
    import templates
    import organisms


# ============================================================================
# DASHBOARD PAGE
# ============================================================================


def dashboard_page(
    page: ft.Page,
    total_users_ref: ft.Ref,
    revenue_ref: ft.Ref,
    orders_ref: ft.Ref,
    growth_ref: ft.Ref,
) -> ft.Row:
    """
    Dashboard page: Main analytics overview.

    This page uses the dashboard template and populates it with:
    - Stats grid organism (with reactive state bindings)
    - Data table organism (with sample data)

    State bindings:
    - page.state.bind("total_users", total_users_ref)
    - page.state.bind("revenue", revenue_ref)
    - page.state.bind("orders", orders_ref)
    - page.state.bind("growth", growth_ref)
    """
    content = ft.Column(
        [
            # Stats overview
            organisms.stats_grid(
                total_users_ref=total_users_ref,
                revenue_ref=revenue_ref,
                orders_ref=orders_ref,
                growth_ref=growth_ref,
            ),
            # Recent orders table
            ft.Container(
                content=organisms.data_table(
                    "Recent Orders",
                    headers=["Order ID", "Customer", "Amount", "Status"],
                    rows=[
                        ["#1001", "John Doe", "$299.00", "Completed"],
                        ["#1002", "Jane Smith", "$450.00", "Processing"],
                        ["#1003", "Bob Johnson", "$150.00", "Completed"],
                        ["#1004", "Alice Brown", "$799.00", "Shipped"],
                        ["#1005", "Charlie Davis", "$99.00", "Pending"],
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=30, vertical=0),
            ),
        ],
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return templates.dashboard_template(
        page,
        current_view="dashboard",
        title="Dashboard",
        content=content,
    )


# ============================================================================
# ANALYTICS PAGE
# ============================================================================


def analytics_page(page: ft.Page) -> ft.Row:
    """
    Analytics page: Detailed analytics view.

    This page demonstrates the full-width template for data-heavy content.
    """
    content = ft.Column(
        [
            ft.Container(
                content=organisms.data_table(
                    "User Analytics",
                    headers=["Metric", "Today", "This Week", "This Month"],
                    rows=[
                        ["Page Views", "1,234", "8,567", "45,890"],
                        ["Unique Visitors", "567", "3,456", "18,234"],
                        ["Avg. Session", "3m 45s", "4m 12s", "3m 58s"],
                        ["Bounce Rate", "45%", "42%", "44%"],
                        ["Conversion Rate", "2.3%", "2.7%", "2.5%"],
                    ],
                ),
                padding=30,
            ),
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return templates.full_width_template(
        page,
        current_view="analytics",
        title="Analytics",
        content=content,
    )


# ============================================================================
# USERS PAGE
# ============================================================================


def users_page(page: ft.Page, search_ref: ft.Ref) -> ft.Row:
    """
    Users page: User management view.

    Demonstrates search functionality and data filtering.
    """
    content = ft.Column(
        [
            ft.Container(
                content=organisms.data_table(
                    "All Users",
                    headers=["ID", "Name", "Email", "Role", "Status"],
                    rows=[
                        ["1", "John Doe", "john@example.com", "Admin", "Active"],
                        ["2", "Jane Smith", "jane@example.com", "User", "Active"],
                        ["3", "Bob Johnson", "bob@example.com", "User", "Inactive"],
                        ["4", "Alice Brown", "alice@example.com", "Manager", "Active"],
                        ["5", "Charlie Davis", "charlie@example.com", "User", "Active"],
                    ],
                ),
                padding=30,
            ),
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return templates.dashboard_template(
        page,
        current_view="users",
        title="Users",
        content=content,
        search_ref=search_ref,
    )


# ============================================================================
# ORDERS PAGE
# ============================================================================


def orders_page(page: ft.Page) -> ft.Row:
    """
    Orders page: Order management view.

    Shows full order history with detailed information.
    """
    content = ft.Column(
        [
            ft.Container(
                content=organisms.data_table(
                    "All Orders",
                    headers=["Order ID", "Customer", "Date", "Amount", "Status"],
                    rows=[
                        ["#1001", "John Doe", "2024-10-15", "$299.00", "Completed"],
                        ["#1002", "Jane Smith", "2024-10-15", "$450.00", "Processing"],
                        ["#1003", "Bob Johnson", "2024-10-14", "$150.00", "Completed"],
                        ["#1004", "Alice Brown", "2024-10-14", "$799.00", "Shipped"],
                        ["#1005", "Charlie Davis", "2024-10-13", "$99.00", "Pending"],
                        [
                            "#1006",
                            "Emma Wilson",
                            "2024-10-13",
                            "$1,250.00",
                            "Completed",
                        ],
                        [
                            "#1007",
                            "Frank Miller",
                            "2024-10-12",
                            "$345.00",
                            "Processing",
                        ],
                        ["#1008", "Grace Lee", "2024-10-12", "$567.00", "Shipped"],
                    ],
                ),
                padding=30,
            ),
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return templates.full_width_template(
        page,
        current_view="orders",
        title="Orders",
        content=content,
    )


# ============================================================================
# SETTINGS PAGE
# ============================================================================


def settings_page(page: ft.Page, name_ref: ft.Ref, email_ref: ft.Ref) -> ft.Row:
    """
    Settings page: User settings and configuration.

    This page uses the centered content template for a focused form experience.

    State bindings:
    - page.state.bind_two_way("user_name", name_ref)
    - page.state.bind_two_way("user_email", email_ref)
    """

    def on_save(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Settings saved successfully!"),
            bgcolor=ft.Colors.GREEN_700,
        )
        page.snack_bar.open = True
        page.update()

    content = ft.Column(
        [
            organisms.settings_form(
                name_ref=name_ref,
                email_ref=email_ref,
                on_save=on_save,
            ),
        ],
        spacing=20,
    )

    return templates.centered_content_template(
        page,
        current_view="settings",
        title="Settings",
        content=content,
        max_width=600,
    )


# ============================================================================
# HELP PAGE
# ============================================================================


def help_page(page: ft.Page) -> ft.Row:
    """
    Help page: Documentation and support.

    Demonstrates centered content with informational text.
    """
    import atoms

    content = ft.Column(
        [
            atoms.card_container(
                content=ft.Column(
                    [
                        atoms.heading2("Getting Started"),
                        atoms.horizontal_divider(),
                        atoms.body_text(
                            "Welcome to the Dashboard! This application is built using the Atomic Design "
                            "methodology with flet-asp for reactive state management."
                        ),
                        ft.Container(height=10),
                        atoms.heading3("Key Features:"),
                        atoms.body_text("• Real-time dashboard metrics"),
                        atoms.body_text("• User and order management"),
                        atoms.body_text("• Advanced analytics"),
                        atoms.body_text("• Customizable settings"),
                        ft.Container(height=10),
                        atoms.heading3("Need Help?"),
                        atoms.body_text(
                            "Contact support at support@example.com or visit our documentation at "
                            "https://github.com/brunobrown/flet-asp"
                        ),
                    ],
                    spacing=15,
                ),
            ),
        ],
        spacing=20,
    )

    return templates.centered_content_template(
        page,
        current_view="help",
        title="Help & Support",
        content=content,
        max_width=700,
    )
