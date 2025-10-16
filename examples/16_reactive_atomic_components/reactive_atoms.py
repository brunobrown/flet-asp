"""
Reactive Atomic Components

Components that combine visual structure (Atomic Design) with reactive state (Flet-ASP).
Each component manages its own state atom and provides a clean API for updates.
"""

import flet as ft
from typing import Optional, Callable, Any


# ============================================================================
# BASE CLASS
# ============================================================================


class ReactiveAtom:
    """
    Base class for reactive atomic components.

    Combines visual component with reactive state management.
    Each component has its own atom and automatically binds to it.
    """

    def __init__(self, page: ft.Page, atom_key: str):
        """
        Initialize reactive component.

        Args:
            page: Flet page instance
            atom_key: Unique key for the state atom
        """
        self.page = page
        self.atom_key = atom_key
        self.control: Optional[ft.Control] = None

    def set(self, value: Any):
        """Update the atom value."""
        self.page.state.set(self.atom_key, value)

    def get(self) -> Any:
        """Get current atom value."""
        return self.page.state.get(self.atom_key)

    def listen(self, callback: Callable, immediate: bool = True):
        """Listen to atom changes."""
        self.page.state.listen(self.atom_key, callback, immediate)


# ============================================================================
# REACTIVE TEXT COMPONENT
# ============================================================================


class ReactiveText(ReactiveAtom):
    """
    Text component with reactive state.

    Automatically updates when the atom value changes.
    """

    def __init__(
        self,
        page: ft.Page,
        atom_key: str,
        initial_value: str = "",
        size: int = 14,
        color: str = None,
        weight: ft.FontWeight = None,
        **kwargs,
    ):
        super().__init__(page, atom_key)

        # Create atom
        page.state.atom(atom_key, initial_value)

        # Create UI
        self.ref = ft.Ref[ft.Text]()
        self.control = ft.Text(
            ref=self.ref,
            value=initial_value,
            size=size,
            color=color,
            weight=weight,
            **kwargs,
        )

        # Bind to state
        page.state.bind(atom_key, self.ref, prop="value")


# ============================================================================
# REACTIVE COUNTER COMPONENT
# ============================================================================


class ReactiveCounter(ReactiveAtom):
    """
    Complete counter component with reactive state.

    Features:
    - Increment/decrement buttons
    - Display with custom styling
    - Configurable step size
    - Reset functionality
    """

    def __init__(
        self,
        page: ft.Page,
        title: str,
        initial_count: int = 0,
        step: int = 1,
        color: str = None,
    ):
        # Generate unique atom key
        atom_key = f"counter_{id(self)}"
        super().__init__(page, atom_key)

        self.step = step
        self.color = color or ft.Colors.BLUE_700

        # Create atom
        page.state.atom(atom_key, initial_count)

        # Create UI
        self.count_ref = ft.Ref[ft.Text]()

        self.control = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        title, size=20, weight=ft.FontWeight.BOLD, color=self.color
                    ),
                    ft.Text(
                        ref=self.count_ref,
                        size=40,
                        color=self.color,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.REMOVE,
                                icon_color=self.color,
                                on_click=self.decrement,
                                tooltip="Decrement",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                icon_color=ft.Colors.GREY_600,
                                on_click=lambda e: self.reset(),
                                tooltip="Reset",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_color=self.color,
                                on_click=self.increment,
                                tooltip="Increment",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border=ft.border.all(2, self.color),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.05, self.color),
        )

        # Bind to state
        page.state.bind(atom_key, self.count_ref, prop="value")

    def increment(self, e=None):
        """Increment counter by step."""
        current = self.get()
        self.set(current + self.step)

    def decrement(self, e=None):
        """Decrement counter by step."""
        current = self.get()
        self.set(current - self.step)

    def reset(self):
        """Reset counter to 0."""
        self.set(0)

    @property
    def value(self) -> int:
        """Get current counter value."""
        return self.get()


# ============================================================================
# REACTIVE STAT CARD COMPONENT
# ============================================================================


class ReactiveStatCard(ReactiveAtom):
    """
    Stat card component with reactive state.

    Perfect for dashboards showing metrics that update automatically.
    """

    def __init__(
        self,
        page: ft.Page,
        title: str,
        atom_key: str,
        initial_value: str = "0",
        icon_name: str = ft.Icons.ANALYTICS,
        color: str = None,
        show_trend: bool = False,
    ):
        super().__init__(page, atom_key)

        self.color = color or ft.Colors.BLUE_700
        self.show_trend = show_trend

        # Create atoms
        page.state.atom(atom_key, initial_value)
        if show_trend:
            page.state.atom(f"{atom_key}_trend", "+0%")

        # Create UI
        self.value_ref = ft.Ref[ft.Text]()
        self.trend_ref = ft.Ref[ft.Text]() if show_trend else None

        # Icon container
        icon_container = ft.Container(
            content=ft.Icon(icon_name, size=32, color=self.color),
            width=64,
            height=64,
            border_radius=32,
            bgcolor=ft.Colors.with_opacity(0.1, self.color),
            alignment=ft.alignment.center,
        )

        # Value column
        value_column = ft.Column(
            [
                ft.Text(title, size=12, color=ft.Colors.GREY_600),
                ft.Text(ref=self.value_ref, size=24, weight=ft.FontWeight.BOLD),
            ],
            spacing=4,
            expand=True,
        )

        # Add trend if enabled
        if show_trend:
            value_column.controls.append(
                ft.Text(ref=self.trend_ref, size=12, color=ft.Colors.GREEN_600)
            )

        self.control = ft.Container(
            content=ft.Row(
                [icon_container, value_column],
                spacing=15,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=3,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

        # Bind to state
        page.state.bind(atom_key, self.value_ref, prop="value")
        if show_trend:
            page.state.bind(f"{atom_key}_trend", self.trend_ref, prop="value")

    def update_with_trend(self, value: str, trend: str):
        """Update value and trend together."""
        self.set(value)
        if self.show_trend:
            self.page.state.set(f"{self.atom_key}_trend", trend)


# ============================================================================
# REACTIVE INPUT COMPONENT
# ============================================================================


class ReactiveInput(ReactiveAtom):
    """
    Input field with reactive two-way binding.

    Changes in the field update the atom, and atom changes update the field.
    """

    def __init__(
        self,
        page: ft.Page,
        atom_key: str,
        initial_value: str = "",
        label: str = None,
        hint: str = None,
        password: bool = False,
        **kwargs,
    ):
        super().__init__(page, atom_key)

        # Create atom
        page.state.atom(atom_key, initial_value)

        # Create UI
        self.ref = ft.Ref[ft.TextField]()
        self.control = ft.TextField(
            ref=self.ref,
            label=label,
            hint_text=hint,
            password=password,
            value=initial_value,
            border_color=ft.Colors.BLUE_700,
            focused_border_color=ft.Colors.BLUE_900,
            **kwargs,
        )

        # Two-way binding
        page.state.bind_two_way(atom_key, self.ref, prop="value")


# ============================================================================
# REACTIVE FORM COMPONENT
# ============================================================================


class ReactiveForm(ReactiveAtom):
    """
    Form component with multiple reactive inputs.

    Manages a group of related inputs with reactive state.
    """

    def __init__(
        self,
        page: ft.Page,
        form_id: str,
        title: str,
        fields: list[dict],
        on_submit: Callable = None,
    ):
        atom_key = f"form_{form_id}"
        super().__init__(page, atom_key)

        self.fields_dict = {}
        self.on_submit = on_submit

        # Create form data atom
        initial_data = {field["key"]: field.get("initial", "") for field in fields}
        page.state.atom(atom_key, initial_data)

        # Create input fields
        inputs = []
        for field in fields:
            field_key = f"{form_id}_{field['key']}"
            reactive_input = ReactiveInput(
                page,
                atom_key=field_key,
                initial_value=field.get("initial", ""),
                label=field.get("label"),
                hint=field.get("hint"),
                password=field.get("password", False),
            )
            self.fields_dict[field["key"]] = reactive_input
            inputs.append(reactive_input.control)

        # Submit button
        submit_btn = ft.ElevatedButton(
            "Submit",
            on_click=self._handle_submit,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        )

        # Create form layout
        self.control = ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    *inputs,
                    ft.Container(height=10),
                    submit_btn,
                ],
                spacing=15,
            ),
            padding=30,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
        )

    def _handle_submit(self, e):
        """Handle form submission."""
        # Collect all field values
        data = {key: field.get() for key, field in self.fields_dict.items()}

        # Update form atom
        self.set(data)

        # Call user callback
        if self.on_submit:
            self.on_submit(data)

    def get_field(self, key: str) -> ReactiveInput:
        """Get a specific field by key."""
        return self.fields_dict.get(key)

    def reset(self):
        """Reset all fields to empty."""
        for field in self.fields_dict.values():
            field.set("")


# ============================================================================
# REACTIVE PROGRESS TRACKER
# ============================================================================


class ReactiveProgress(ReactiveAtom):
    """
    Progress tracker with reactive state.

    Automatically updates progress bar and percentage.
    """

    def __init__(
        self,
        page: ft.Page,
        atom_key: str,
        title: str = "Progress",
        max_value: int = 100,
        color: str = None,
    ):
        super().__init__(page, atom_key)

        self.max_value = max_value
        self.color = color or ft.Colors.BLUE_700

        # Create atom
        page.state.atom(atom_key, 0)

        # Create UI
        self.progress_ref = ft.Ref[ft.ProgressBar]()
        self.text_ref = ft.Ref[ft.Text]()

        self.control = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            title, size=16, weight=ft.FontWeight.W_600, expand=True
                        ),
                        ft.Text(ref=self.text_ref, size=16, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.ProgressBar(
                    ref=self.progress_ref,
                    value=0,
                    color=self.color,
                    bgcolor=ft.Colors.GREY_200,
                    height=8,
                    bar_height=8,
                ),
            ],
            spacing=10,
        )

        # Custom binding with transformation
        # Since bind_dynamic doesn't support transform functions,
        # we use listen() to manually update the controls
        def update_progress(value):
            if self.progress_ref.current:
                self.progress_ref.current.value = value / self.max_value
            if self.text_ref.current:
                self.text_ref.current.value = f"{int((value / self.max_value) * 100)}%"
            page.update()

        page.state.listen(atom_key, update_progress, immediate=True)

    def increment(self, amount: int = 1):
        """Increment progress."""
        current = self.get()
        new_value = min(current + amount, self.max_value)
        self.set(new_value)

    def complete(self):
        """Set progress to 100%."""
        self.set(self.max_value)

    def reset(self):
        """Reset progress to 0."""
        self.set(0)
