"""
Example 16: Reactive Atomic Components

This example demonstrates components that combine Atomic Design (visual structure)
with Flet-ASP reactive state (automatic updates).

Key Features:
- ReactiveCounter: Counter with built-in state
- ReactiveStatCard: Dashboard metrics with auto-updates
- ReactiveInput: Form inputs with two-way binding
- ReactiveForm: Complete forms with validation
- ReactiveProgress: Progress trackers

All components manage their own state atoms and provide a clean API!

Run this example:
    python examples/16_reactive_atomic_components/main.py

Or as a module:
    python -m examples.16_reactive_atomic_components.main
"""

import flet as ft
import flet_asp as fa
import threading
import time
import random

# Handle both direct execution and module import
try:
    from .reactive_atoms import (
        ReactiveCounter,
        ReactiveStatCard,
        ReactiveForm,
        ReactiveProgress,
        ReactiveText,
    )
except ImportError:
    from reactive_atoms import (
        ReactiveCounter,
        ReactiveStatCard,
        ReactiveForm,
        ReactiveProgress,
        ReactiveText,
    )


def main(page: ft.Page):
    """Main application entry point."""
    page.title = "Reactive Atomic Components"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Initialize state manager
    fa.get_state_manager(page)

    # ========================================================================
    # SECTION 1: REACTIVE COUNTERS
    # ========================================================================

    section1_title = ft.Text(
        "🔢 Reactive Counters",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_900,
    )

    section1_desc = ft.Text(
        "Each counter is a self-contained component with reactive state.\n"
        "No manual binding needed - just create and use!",
        size=14,
        color=ft.Colors.GREY_700,
    )

    # Create reactive counters
    counter_a = ReactiveCounter(
        page, title="Counter A", initial_count=0, step=1, color=ft.Colors.BLUE_700
    )

    counter_b = ReactiveCounter(
        page, title="Counter B", initial_count=10, step=5, color=ft.Colors.GREEN_700
    )

    counter_c = ReactiveCounter(
        page, title="Counter C", initial_count=100, step=10, color=ft.Colors.PURPLE_700
    )

    # Sum display (computed from counters)
    sum_text = ReactiveText(
        page,
        atom_key="counter_sum",
        initial_value="0",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ORANGE_700,
    )

    def update_sum():
        """Update sum whenever any counter changes."""
        total = counter_a.value + counter_b.value + counter_c.value
        sum_text.set(f"Total: {total}")

    # Listen to counter changes
    counter_a.listen(lambda _: update_sum(), immediate=True)
    counter_b.listen(lambda _: update_sum(), immediate=True)
    counter_c.listen(lambda _: update_sum(), immediate=True)

    section1 = ft.Container(
        content=ft.Column(
            [
                section1_title,
                section1_desc,
                ft.Container(height=20),
                ft.Row(
                    [counter_a.control, counter_b.control, counter_c.control],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    spacing=20,
                ),
                ft.Container(height=10),
                ft.Container(
                    content=sum_text.control,
                    alignment=ft.alignment.center,
                    padding=20,
                    border_radius=8,
                    bgcolor=ft.Colors.ORANGE_50,
                    border=ft.border.all(2, ft.Colors.ORANGE_200),
                ),
            ]
        ),
        padding=30,
        margin=ft.margin.only(bottom=30),
        border_radius=12,
        bgcolor=ft.Colors.BLUE_50,
        border=ft.border.all(1, ft.Colors.BLUE_200),
    )

    # ========================================================================
    # SECTION 2: REACTIVE STAT CARDS (DASHBOARD)
    # ========================================================================

    section2_title = ft.Text(
        "📊 Reactive Dashboard",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_900,
    )

    section2_desc = ft.Text(
        "Stat cards that automatically update every 3 seconds.\n"
        "Perfect for real-time dashboards!",
        size=14,
        color=ft.Colors.GREY_700,
    )

    # Create reactive stat cards
    users_card = ReactiveStatCard(
        page,
        title="Total Users",
        atom_key="total_users",
        initial_value="1,234",
        icon_name=ft.Icons.PEOPLE,
        color=ft.Colors.BLUE_700,
        show_trend=True,
    )

    revenue_card = ReactiveStatCard(
        page,
        title="Revenue",
        atom_key="revenue",
        initial_value="$45,678",
        icon_name=ft.Icons.ATTACH_MONEY,
        color=ft.Colors.GREEN_700,
        show_trend=True,
    )

    orders_card = ReactiveStatCard(
        page,
        title="Orders",
        atom_key="orders",
        initial_value="892",
        icon_name=ft.Icons.SHOPPING_CART,
        color=ft.Colors.ORANGE_700,
        show_trend=True,
    )

    growth_card = ReactiveStatCard(
        page,
        title="Growth",
        atom_key="growth",
        initial_value="+12.5%",
        icon_name=ft.Icons.TRENDING_UP,
        color=ft.Colors.PURPLE_700,
        show_trend=False,
    )

    # Auto-update thread
    def auto_update_stats():
        """Simulate real-time data updates."""
        while True:
            time.sleep(3)
            try:
                users_card.update_with_trend(
                    f"{random.randint(1000, 2000):,}", f"+{random.randint(5, 20)}%"
                )
                revenue_card.update_with_trend(
                    f"${random.randint(40000, 60000):,}", f"+{random.randint(3, 15)}%"
                )
                orders_card.update_with_trend(
                    f"{random.randint(800, 1000)}", f"+{random.randint(1, 10)}%"
                )
                growth_card.set(f"+{random.randint(10, 25)}.{random.randint(0, 9)}%")
            except Exception:
                break

    stats_thread = threading.Thread(target=auto_update_stats, daemon=True)
    stats_thread.start()

    section2 = ft.Container(
        content=ft.Column(
            [
                section2_title,
                section2_desc,
                ft.Container(height=20),
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            users_card.control, col={"sm": 12, "md": 6, "lg": 3}
                        ),
                        ft.Container(
                            revenue_card.control, col={"sm": 12, "md": 6, "lg": 3}
                        ),
                        ft.Container(
                            orders_card.control, col={"sm": 12, "md": 6, "lg": 3}
                        ),
                        ft.Container(
                            growth_card.control, col={"sm": 12, "md": 6, "lg": 3}
                        ),
                    ],
                    spacing=20,
                    run_spacing=20,
                ),
            ]
        ),
        padding=30,
        margin=ft.margin.only(bottom=30),
        border_radius=12,
        bgcolor=ft.Colors.GREEN_50,
        border=ft.border.all(1, ft.Colors.GREEN_200),
    )

    # ========================================================================
    # SECTION 3: REACTIVE FORM
    # ========================================================================

    section3_title = ft.Text(
        "📝 Reactive Form",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_900,
    )

    section3_desc = ft.Text(
        "Form with reactive inputs. All fields have two-way binding!\n"
        "Changes sync automatically with state atoms.",
        size=14,
        color=ft.Colors.GREY_700,
    )

    form_result_text = ft.Ref[ft.Text]()

    # Atom for form result - declarative approach
    page.state.atom("form_result", "")

    def handle_form_submit(data):
        """Handle form submission."""
        result = (
            f"✅ Form Submitted!\n\n"
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Password: {'*' * len(data['password'])}"
        )
        page.state.set("form_result", result)  # No page.update() needed

    # Create reactive form
    user_form = ReactiveForm(
        page,
        form_id="user_registration",
        title="User Registration",
        fields=[
            {"key": "name", "label": "Full Name", "hint": "Enter your name"},
            {"key": "email", "label": "Email", "hint": "your@email.com"},
            {
                "key": "password",
                "label": "Password",
                "password": True,
                "hint": "Min 8 characters",
            },
        ],
        on_submit=handle_form_submit,
    )

    section3 = ft.Container(
        content=ft.Column(
            [
                section3_title,
                section3_desc,
                ft.Container(height=20),
                ft.Row(
                    [
                        ft.Container(user_form.control, expand=1),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Form Result:",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Divider(),
                                    ft.Text(
                                        ref=form_result_text,
                                        value="Submit the form to see results here",
                                        color=ft.Colors.GREY_600,
                                    ),
                                ]
                            ),
                            padding=20,
                            border_radius=12,
                            bgcolor=ft.Colors.GREY_100,
                            expand=1,
                        ),
                    ],
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ]
        ),
        padding=30,
        margin=ft.margin.only(bottom=30),
        border_radius=12,
        bgcolor=ft.Colors.PURPLE_50,
        border=ft.border.all(1, ft.Colors.PURPLE_200),
    )

    # Bind form result to text - declarative, no page.update() needed
    page.state.bind("form_result", form_result_text, prop="value")

    # ========================================================================
    # SECTION 4: REACTIVE PROGRESS
    # ========================================================================

    section4_title = ft.Text(
        "⏳ Reactive Progress Tracker",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ORANGE_900,
    )

    section4_desc = ft.Text(
        "Progress bars with reactive state. Watch them update automatically!",
        size=14,
        color=ft.Colors.GREY_700,
    )

    # Create progress trackers
    upload_progress = ReactiveProgress(
        page,
        atom_key="upload_progress",
        title="Upload Progress",
        max_value=100,
        color=ft.Colors.BLUE_700,
    )

    download_progress = ReactiveProgress(
        page,
        atom_key="download_progress",
        title="Download Progress",
        max_value=100,
        color=ft.Colors.GREEN_700,
    )

    def simulate_upload(e):
        """Simulate file upload."""
        upload_progress.reset()

        def upload():
            for i in range(0, 101, 5):
                time.sleep(0.1)
                upload_progress.set(i)

        threading.Thread(target=upload, daemon=True).start()

    def simulate_download(e):
        """Simulate file download."""
        download_progress.reset()

        def download():
            for i in range(0, 101, 3):
                time.sleep(0.15)
                download_progress.set(i)

        threading.Thread(target=download, daemon=True).start()

    section4 = ft.Container(
        content=ft.Column(
            [
                section4_title,
                section4_desc,
                ft.Container(height=20),
                upload_progress.control,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Simulate Upload",
                    on_click=simulate_upload,
                    icon=ft.Icons.UPLOAD,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE
                    ),
                ),
                ft.Container(height=30),
                download_progress.control,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Simulate Download",
                    on_click=simulate_download,
                    icon=ft.Icons.DOWNLOAD,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE
                    ),
                ),
            ]
        ),
        padding=30,
        margin=ft.margin.only(bottom=30),
        border_radius=12,
        bgcolor=ft.Colors.ORANGE_50,
        border=ft.border.all(1, ft.Colors.ORANGE_200),
    )

    # ========================================================================
    # ADD ALL SECTIONS TO PAGE
    # ========================================================================

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Reactive Atomic Components",
                                size=40,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                            ft.Text(
                                "Components that combine Atomic Design + Flet-ASP reactive state",
                                size=16,
                                color=ft.Colors.GREY_700,
                            ),
                        ]
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                ),
                ft.Divider(height=20),
                section1,
                section2,
                section3,
                section4,
                ft.Container(
                    content=ft.Text(
                        "Flet-ASP",
                        size=14,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=20,
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
