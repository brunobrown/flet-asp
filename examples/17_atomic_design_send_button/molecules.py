"""
Molecules - Simple combinations of atoms that work as functional units.
Following the Atomic Design pattern with Flet-ASP.

Uses:
- atom() for base state (hover, icon_offset for floating animation)
- selector() for derived states (rotate, scale, text_offset, text_opacity)
- bind() to link components to reactive state
"""

import flet as ft
from atoms import send_icon, button_text, cloud_icon, loading_bar


class SendIconWithText:
    """
    Molecule: Combination of send icon with text.

    Uses selectors to automatically derive visual states from hover state.
    The icon_offset is a separate atom because it's controlled by the floating animation.
    """

    def __init__(
        self,
        page: ft.Page,
        prefix: str = "send_btn",
        text_value: str = "SEND",
        icon_size: int = 16,
        text_size: int = 14,
        color: str = ft.Colors.WHITE,
        initial_rotation: float = 11,
        hover_rotation: float = 12.5,
    ):
        self.page = page
        self.prefix = prefix
        self.initial_rotation = initial_rotation
        self.hover_rotation = hover_rotation

        # Create refs for binding
        self.icon_ref = ft.Ref[ft.IconButton]()
        self.text_ref = ft.Ref[ft.Text]()

        # Create UI atoms
        self.icon = send_icon(
            ref=self.icon_ref,
            size=icon_size,
            color=color,
            initial_rotation=initial_rotation,
        )
        self.text = button_text(
            ref=self.text_ref,
            value=text_value,
            size=text_size,
            color=color,
        )

        # Create reactive state atoms and selectors
        self._setup_state()

    def _setup_state(self):
        """Configures base atoms and derived selectors."""
        # === BASE ATOMS ===
        # Hover state - controls derived visual states
        self.page.state.atom(f"{self.prefix}_hover", False)

        # Loading state - also controls derived visual states
        self.page.state.atom(f"{self.prefix}_loading", False)

        # Icon offset - separate atom because it's controlled by the floating animation
        # (doesn't depend only on hover, but also on time)
        self.page.state.atom(f"{self.prefix}_icon_offset", ft.Offset(0, 0))

        # === SELECTORS - States automatically derived from hover or loading ===

        # Icon rotation derived from hover or loading
        @self.page.state.selector(f"{self.prefix}_icon_rotate")
        def compute_icon_rotate(get):
            is_hover = get(f"{self.prefix}_hover")
            is_loading = get(f"{self.prefix}_loading")
            rotation = (
                self.hover_rotation
                if (is_hover or is_loading)
                else self.initial_rotation
            )
            return ft.Rotate(rotation, alignment=ft.alignment.center)

        # Icon scale derived from hover or loading
        @self.page.state.selector(f"{self.prefix}_icon_scale")
        def compute_icon_scale(get):
            is_hover = get(f"{self.prefix}_hover")
            is_loading = get(f"{self.prefix}_loading")
            return ft.Scale(1.25 if (is_hover or is_loading) else 1)

        # Text offset derived from hover or loading
        @self.page.state.selector(f"{self.prefix}_text_offset")
        def compute_text_offset(get):
            is_hover = get(f"{self.prefix}_hover")
            is_loading = get(f"{self.prefix}_loading")
            return ft.Offset(1, 0) if (is_hover or is_loading) else ft.Offset(-0.4, 0)

        # Text opacity derived from hover or loading
        @self.page.state.selector(f"{self.prefix}_text_opacity")
        def compute_text_opacity(get):
            is_hover = get(f"{self.prefix}_hover")
            is_loading = get(f"{self.prefix}_loading")
            return 0.0 if (is_hover or is_loading) else 1.0

        # === BINDINGS ===
        # Bind refs to atoms/selectors for automatic updates
        self.page.state.bind(f"{self.prefix}_icon_offset", self.icon_ref, "offset")
        self.page.state.bind(f"{self.prefix}_icon_rotate", self.icon_ref, "rotate")
        self.page.state.bind(f"{self.prefix}_icon_scale", self.icon_ref, "scale")
        self.page.state.bind(f"{self.prefix}_text_offset", self.text_ref, "offset")
        self.page.state.bind(f"{self.prefix}_text_opacity", self.text_ref, "opacity")

    def set_hover_state(self, is_hovering: bool):
        """
        Updates the hover state.

        All visual states (rotate, scale, text_offset, text_opacity)
        are automatically derived via selectors.
        """
        self.page.state.set(f"{self.prefix}_hover", is_hovering)

    def set_loading_state(self, is_loading: bool):
        """
        Updates the loading state.

        All visual states (rotate, scale, text_offset, text_opacity)
        are automatically derived via selectors.
        """
        self.page.state.set(f"{self.prefix}_loading", is_loading)

    def set_icon_offset(self, x: float, y: float):
        """Sets the icon offset (used by floating animation)."""
        self.page.state.set(f"{self.prefix}_icon_offset", ft.Offset(x, y))

    def is_hovering(self) -> bool:
        """Returns whether it's in hover state."""
        return self.page.state.get(f"{self.prefix}_hover")

    def is_loading(self) -> bool:
        """Returns whether it's in loading state."""
        return self.page.state.get(f"{self.prefix}_loading")

    def build(self) -> ft.Row:
        """Returns the Row component with icon and text."""
        return ft.Row(
            controls=[self.icon, self.text],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )


class CloudPair:
    """
    Molecule: Cloud pair for alternating parallax effect.

    Uses atoms with incremental counter to avoid deep_equal blocking.
    Each cloud has its own state (left, opacity) linked via bind().
    """

    def __init__(
        self,
        page: ft.Page,
        prefix: str = "cloud",
        size: int = 12,
        color: str = ft.Colors.WHITE54,
        top: int = None,
        bottom: int = None,
        animation_duration: int = 1200,
    ):
        self.page = page
        self.prefix = prefix
        self.animation_duration = animation_duration
        self._current_idx = 0
        self._counter_a = 0
        self._counter_b = 0

        # Create refs
        self.cloud_a_ref = ft.Ref[ft.Container]()
        self.cloud_b_ref = ft.Ref[ft.Container]()

        # Create UI atoms
        self.cloud_a = cloud_icon(
            ref=self.cloud_a_ref,
            size=size,
            color=color,
            top=top,
            bottom=bottom,
            animation_duration=animation_duration,
        )
        self.cloud_b = cloud_icon(
            ref=self.cloud_b_ref,
            size=size,
            color=color,
            top=top,
            bottom=bottom,
            animation_duration=animation_duration,
        )

        # Create state atoms
        self._setup_state()

    def _setup_state(self):
        """
        Configures atoms for each cloud.
        Binds directly to left and opacity atoms (simple values).
        The incremental counter ensures each set() is unique.
        """
        # Separate atoms for each property of each cloud
        # Using tuple (value, counter) to ensure uniqueness
        self.page.state.atom(f"{self.prefix}_a_left", (130, 0))
        self.page.state.atom(f"{self.prefix}_a_opacity", (0.0, 0))
        self.page.state.atom(f"{self.prefix}_b_left", (130, 0))
        self.page.state.atom(f"{self.prefix}_b_opacity", (0.0, 0))

        # Selectors that extract only the value (first element of the tuple)
        @self.page.state.selector(f"{self.prefix}_a_left_val")
        def get_a_left(get):
            return get(f"{self.prefix}_a_left")[0]

        @self.page.state.selector(f"{self.prefix}_a_opacity_val")
        def get_a_opacity(get):
            return get(f"{self.prefix}_a_opacity")[0]

        @self.page.state.selector(f"{self.prefix}_b_left_val")
        def get_b_left(get):
            return get(f"{self.prefix}_b_left")[0]

        @self.page.state.selector(f"{self.prefix}_b_opacity_val")
        def get_b_opacity(get):
            return get(f"{self.prefix}_b_opacity")[0]

        # Bindings using selectors
        self.page.state.bind(f"{self.prefix}_a_left_val", self.cloud_a_ref, "left")
        self.page.state.bind(
            f"{self.prefix}_a_opacity_val", self.cloud_a_ref, "opacity"
        )
        self.page.state.bind(f"{self.prefix}_b_left_val", self.cloud_b_ref, "left")
        self.page.state.bind(
            f"{self.prefix}_b_opacity_val", self.cloud_b_ref, "opacity"
        )

    def _set_cloud_state(self, suffix: str, left: float, opacity: float):
        """Updates cloud state via separate atoms (with unique counter)."""
        if suffix == "a":
            self._counter_a += 1
            self.page.state.set(f"{self.prefix}_a_left", (left, self._counter_a))
            self.page.state.set(f"{self.prefix}_a_opacity", (opacity, self._counter_a))
        else:
            self._counter_b += 1
            self.page.state.set(f"{self.prefix}_b_left", (left, self._counter_b))
            self.page.state.set(f"{self.prefix}_b_opacity", (opacity, self._counter_b))

    def get_clouds(self) -> list:
        """Returns list with both clouds."""
        return [self.cloud_a, self.cloud_b]

    def get_next_cloud_suffix(self) -> str:
        """Returns the suffix of the next cloud in the cycle."""
        suffix = "a" if self._current_idx == 0 else "b"
        self._current_idx = (self._current_idx + 1) % 2
        return suffix

    def set_cloud_position(self, suffix: str, left: float, opacity: float):
        """Sets cloud position and opacity via reactive state."""
        self._set_cloud_state(suffix, left, opacity)

    def reset(self):
        """Resets both clouds to initial position (hidden)."""
        self._set_cloud_state("a", 130, 0.0)
        self._set_cloud_state("b", 130, 0.0)

    def get_animation_duration_seconds(self) -> float:
        """Returns the animation duration in seconds."""
        return self.animation_duration / 1000


class LoadingBar:
    """
    Molecule: Loading bar with progress controlled via flet-asp.

    Uses atom for progress (0-100) and bind to update bar width.
    """

    def __init__(
        self,
        page: ft.Page,
        prefix: str = "loading",
        width: int = 130,
        height: int = 6,
        bgcolor: str = ft.Colors.BLUE_300,
        bar_color: str = ft.Colors.WHITE,
    ):
        self.page = page
        self.prefix = prefix
        self.width = width
        self._counter = 0  # Counter to ensure uniqueness in deep_equal

        # Create refs
        self.bar_ref = ft.Ref[ft.Container]()
        self.progress_ref = ft.Ref[ft.ProgressBar]()

        # Create UI atom (passing both refs)
        self.bar = loading_bar(
            ref=self.bar_ref,
            progress_ref=self.progress_ref,  # Ref for the ProgressBar
            width=width,
            height=height,
            bgcolor=bgcolor,
            bar_color=bar_color,
        )

        # Create reactive state
        self._setup_state()

    def _setup_state(self):
        """Configures progress atom, visibility, and selectors."""
        # Atom: progress from 0 to 100 with counter (value, counter)
        self.page.state.atom(f"{self.prefix}_progress", (0.0, 0))

        # Atom: visibility (True = visible, False = hidden)
        self.page.state.atom(f"{self.prefix}_visible", False)

        # Selector: converts progress (0-100) to ProgressBar value (0.0-1.0)
        @self.page.state.selector(f"{self.prefix}_value")
        def compute_value(get):
            progress_tuple = get(f"{self.prefix}_progress")
            progress = progress_tuple[0]  # Extract value from tuple (0-100)
            return progress / 100.0  # Convert to 0.0-1.0

        # Selector: opacity based on visibility
        @self.page.state.selector(f"{self.prefix}_opacity")
        def compute_opacity(get):
            return 1.0 if get(f"{self.prefix}_visible") else 0.0

        # Bindings
        self.page.state.bind(f"{self.prefix}_value", self.progress_ref, "value")
        self.page.state.bind(f"{self.prefix}_opacity", self.bar_ref, "opacity")

    def set_progress(self, progress: float):
        """Sets the bar progress (0-100)."""
        progress = max(0, min(100, progress))  # Clamp between 0-100
        self._counter += 1

        # Update only the atom - flet-asp should manage the update
        self.page.state.set(f"{self.prefix}_progress", (progress, self._counter))

    def show(self):
        """Makes the bar visible."""
        self.page.state.set(f"{self.prefix}_visible", True)

    def hide(self):
        """Hides the bar."""
        self.page.state.set(f"{self.prefix}_visible", False)

    def reset(self):
        """Resets the bar to 0%."""
        self.set_progress(0)

    def build(self) -> ft.Container:
        """Returns the bar component."""
        return self.bar
