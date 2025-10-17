"""
Example 14: Atomic Design System Dashboard

A complete dashboard application demonstrating the Atomic Design methodology
with flet-asp reactive state management.

ATOMIC DESIGN HIERARCHY:
========================

Atoms (atoms.py)
  └─ Basic elements: buttons, inputs, text, icons, dividers
      ↓
Molecules (molecules.py)
  └─ Simple combinations: stat cards, menu items, form fields, search bars
      ↓
Organisms (organisms.py)
  └─ Complex components: sidebar, top bar, stats grid, data tables
      ↓
Templates (templates.py)
  └─ Page layouts: dashboard template, centered template, full-width template
      ↓
Pages (pages.py)
  └─ Complete screens: dashboard, analytics, users, orders, settings, help

STATE MANAGEMENT WITH FLET-ASP:
================================

This example shows how Atomic Design works seamlessly with reactive state:
- Atoms are bound to state values for real-time updates
- State changes propagate through the component hierarchy
- Two-way binding keeps forms in sync with state
- Multiple pages share the same state atoms

Run this example:
    python examples/14_atomic_design_dashboard/main.py

Or from the parent directory:
    python -m examples.14_atomic_design_dashboard.main
"""

import flet as ft
import flet_asp as fa

# Handle both direct execution and module import
try:
    from . import pages
except ImportError:
    import pages


def main(page: ft.Page):
    """Main application entry point."""
    page.title = "Atomic Design Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # Initialize state manager
    fa.get_state_manager(page)

    # ========================================================================
    # STATE ATOMS
    # ========================================================================

    # Dashboard metrics (bound to stat cards)
    page.state.atom("total_users", "1,234")
    page.state.atom("revenue", "$45,678")
    page.state.atom("orders", "892")
    page.state.atom("growth", "+12.5%")

    # Settings form (two-way binding)
    page.state.atom("user_name", "Admin User")
    page.state.atom("user_email", "admin@example.com")

    # Navigation state
    page.state.atom("current_view", "dashboard")

    # Search state
    page.state.atom("search_query", "")

    # ========================================================================
    # REFS FOR UI BINDINGS
    # ========================================================================

    # Dashboard metrics refs
    total_users_ref = ft.Ref[ft.Text]()
    revenue_ref = ft.Ref[ft.Text]()
    orders_ref = ft.Ref[ft.Text]()
    growth_ref = ft.Ref[ft.Text]()

    # Settings form refs
    name_ref = ft.Ref[ft.TextField]()
    email_ref = ft.Ref[ft.TextField]()

    # Search ref
    search_ref = ft.Ref[ft.TextField]()

    # ========================================================================
    # BINDINGS
    # ========================================================================
    # Note: Bindings will be set up when each page is rendered

    # ========================================================================
    # VIEW ROUTING
    # ========================================================================

    def render_view(view_name: str):
        """Render the appropriate page based on current view."""
        page.controls.clear()

        if view_name == "dashboard":
            page.add(
                pages.dashboard_page(
                    page,
                    total_users_ref,
                    revenue_ref,
                    orders_ref,
                    growth_ref,
                )
            )
            # Bind dashboard metrics
            page.state.bind("total_users", total_users_ref, prop="value")
            page.state.bind("revenue", revenue_ref, prop="value")
            page.state.bind("orders", orders_ref, prop="value")
            page.state.bind("growth", growth_ref, prop="value")
        elif view_name == "analytics":
            page.add(pages.analytics_page(page))
        elif view_name == "users":
            page.add(pages.users_page(page, search_ref))
            # Bind search
            page.state.bind_two_way("search_query", search_ref, prop="value")
        elif view_name == "orders":
            page.add(pages.orders_page(page))
        elif view_name == "settings":
            page.add(pages.settings_page(page, name_ref, email_ref))
            # Bind settings form
            page.state.bind_two_way("user_name", name_ref, prop="value")
            page.state.bind_two_way("user_email", email_ref, prop="value")
        elif view_name == "help":
            page.add(pages.help_page(page))
        else:
            page.add(
                pages.dashboard_page(
                    page,
                    total_users_ref,
                    revenue_ref,
                    orders_ref,
                    growth_ref,
                )
            )
            # Bind dashboard metrics
            page.state.bind("total_users", total_users_ref, prop="value")
            page.state.bind("revenue", revenue_ref, prop="value")
            page.state.bind("orders", orders_ref, prop="value")
            page.state.bind("growth", growth_ref, prop="value")

        page.update()

    # Listen to view changes
    page.state.listen("current_view", lambda value: render_view(value))

    # ========================================================================
    # SIMULATE LIVE DATA UPDATES
    # ========================================================================

    import random

    def update_metrics(e):
        """Simulate real-time metric updates."""
        page.state.set("total_users", f"{random.randint(1000, 2000):,}")
        page.state.set("revenue", f"${random.randint(40000, 60000):,}")
        page.state.set("orders", f"{random.randint(800, 1000)}")
        page.state.set("growth", f"+{random.randint(10, 20)}.{random.randint(0, 9)}%")

    # Update metrics every 5 seconds
    import threading
    import time

    def auto_update():
        while True:
            time.sleep(5)
            try:
                update_metrics(None)
            except Exception:
                break

    # Start background thread for live updates
    thread = threading.Thread(target=auto_update, daemon=True)
    thread.start()

    # ========================================================================
    # INITIAL RENDER
    # ========================================================================

    render_view("dashboard")


if __name__ == "__main__":
    ft.app(target=main)
