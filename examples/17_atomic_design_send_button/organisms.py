"""
Organisms - Complex components composed of molecules and atoms.
Following the Atomic Design pattern with Flet-ASP.

Uses Flet lifecycle methods:
- build(): Builds the UI when the control receives self.page
- did_mount(): Starts animations after the control is added to the page
- will_unmount(): Stops animations before the control is removed
"""

import time
import flet as ft
from molecules import SendIconWithText, CloudPair, LoadingBar


class AnimatedSendButton(ft.Container):
    """
    Organism: Animated send button with cloud parallax effect and loading.

    Composite custom control that inherits from Container and uses:
    - Flet lifecycle (build, did_mount, will_unmount)
    - flet_asp reactive state for UI updates
    - Does not use update() directly - all changes are via atoms

    Combines:
    - SendIconWithText (molecule): airplane icon + "SEND" text
    - CloudPair (molecule): cloud pairs for parallax
    - LoadingBar (molecule): progress bar
    """

    def __init__(
        self,
        width: int = 130,
        height: int = 45,
        bgcolor: str = ft.Colors.BLUE_700,
        text_value: str = "SEND",
        float_interval: float = 0.5,
        loading_duration: float = 3.0,
    ):
        super().__init__()
        self.prefix = "animated_btn"
        self._width = width
        self._height = height
        self._bgcolor = bgcolor
        self._text_value = text_value
        self._float_interval = float_interval
        self._loading_duration = loading_duration
        self._running = False
        self._is_loading = False

        # Molecules will be created in build()
        self.send_icon_text = None
        self.clouds_top = None
        self.clouds_bottom = None
        self.loading_bar = None

    def build(self):
        """
        Builds the UI when the control receives self.page.
        Here we have access to self.page to create state atoms.
        """
        # Create molecules with unique prefixes
        self.send_icon_text = SendIconWithText(
            page=self.page,
            prefix=f"{self.prefix}_icon_text",
            text_value=self._text_value,
        )

        # Top clouds (faster)
        self.clouds_top = CloudPair(
            page=self.page,
            prefix=f"{self.prefix}_cloud_top",
            size=12,
            color=ft.Colors.WHITE54,
            top=8,
            animation_duration=1200,
        )

        # Bottom clouds (slower - parallax)
        self.clouds_bottom = CloudPair(
            page=self.page,
            prefix=f"{self.prefix}_cloud_bottom",
            size=10,
            color=ft.Colors.WHITE38,
            bottom=8,
            animation_duration=1800,
        )

        # Loading bar
        self.loading_bar = LoadingBar(
            page=self.page,
            prefix=f"{self.prefix}_loading",
            width=self._width,
            height=6,
            bgcolor=ft.Colors.BLUE_300,
            bar_color=ft.Colors.WHITE,
        )

        # Configure Container properties (self) - back to single Container
        self.width = self._width
        self.height = self._height
        self.bgcolor = self._bgcolor
        self.border_radius = 10
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.on_hover = self._on_hover
        self.content = ft.Stack(
            controls=[
                # Cloud layer (background)
                *self.clouds_top.get_clouds(),
                *self.clouds_bottom.get_clouds(),
                # Icon and text layer (middle)
                self.send_icon_text.build(),
                # Loading bar (front, at the bottom)
                ft.Container(
                    content=self.loading_bar.build(),
                    bottom=0,
                    left=0,
                    right=0,
                ),
                # Transparent layer to capture clicks (covers everything)
                ft.Container(
                    width=self._width,
                    height=self._height,
                    bgcolor=ft.Colors.TRANSPARENT,
                    on_click=self._on_click,
                ),
            ],
        )

    def did_mount(self):
        """
        Called after the control is added to the page.
        Starts the animation threads here.
        """
        self._running = True
        self.page.run_thread(self._fly_animation)
        self.page.run_thread(self._cloud_top_animation)
        self.page.run_thread(self._cloud_bottom_animation)

    def will_unmount(self):
        """
        Called before the control is removed from the page.
        Stops the animation threads.
        """
        self._running = False

    def _on_hover(self, e):
        """Hover event handler - uses reactive state."""
        is_hovering = e.data == "true"
        self.send_icon_text.set_hover_state(is_hovering)

    def _on_click(self, e):
        """Click handler - starts loading."""
        if not self._is_loading:
            self._is_loading = True

            # Activate loading state on icon/text (hides text and centers icon)
            self.send_icon_text.set_loading_state(True)

            # Reset and show bar immediately
            self.loading_bar.reset()
            self.loading_bar.show()

            # Start loading in thread
            self.page.run_thread(self._loading_animation)

    @staticmethod
    def _animate_cloud(cloud_pair: CloudPair, duration: float):
        """Animates a cloud from right to left."""
        suffix = cloud_pair.get_next_cloud_suffix()

        # Position on the right (invisible)
        cloud_pair.set_cloud_position(suffix, 130, 0.0)
        time.sleep(0.05)

        # Show and move to the left
        cloud_pair.set_cloud_position(suffix, -20, 1.0)
        time.sleep(duration)

        # Hide when reaching the left
        cloud_pair.set_cloud_position(suffix, 130, 0.0)
        time.sleep(0.05)

    def _fly_animation(self):
        """Thread: Flying/floating airplane effect - always active."""
        while self._running:
            is_hover = self.send_icon_text.is_hovering()
            is_loading = self._is_loading

            if is_hover or is_loading:
                # Floating when hover or loading (centered)
                self.send_icon_text.set_icon_offset(0.5, 0.09)
                time.sleep(self._float_interval)

                if self._running and (
                    self.send_icon_text.is_hovering() or self._is_loading
                ):
                    self.send_icon_text.set_icon_offset(0.5, -0.09)
                    time.sleep(self._float_interval)
            else:
                # Normal floating (initial position)
                self.send_icon_text.set_icon_offset(0, 0.09)
                time.sleep(self._float_interval)

                if (
                    self._running
                    and not self.send_icon_text.is_hovering()
                    and not self._is_loading
                ):
                    self.send_icon_text.set_icon_offset(0, -0.09)
                    time.sleep(self._float_interval)

    def _cloud_top_animation(self):
        """Thread: Top clouds parallax effect."""
        while self._running:
            if self.send_icon_text.is_hovering() or self._is_loading:
                self._animate_cloud(
                    self.clouds_top, self.clouds_top.get_animation_duration_seconds()
                )
            else:
                self.clouds_top.reset()
                time.sleep(0.1)

    def _cloud_bottom_animation(self):
        """Thread: Bottom clouds parallax effect."""
        while self._running:
            if self.send_icon_text.is_hovering() or self._is_loading:
                self._animate_cloud(
                    self.clouds_bottom,
                    self.clouds_bottom.get_animation_duration_seconds(),
                )
            else:
                self.clouds_bottom.reset()
                time.sleep(0.1)

    def _loading_animation(self):
        """Thread: Progressive loading animation."""
        # Simulate loading with incremental progress
        steps = 100
        delay = self._loading_duration / steps

        for i in range(steps + 1):
            if not self._running:
                break
            self.loading_bar.set_progress(i)
            time.sleep(delay)

        # Hide bar and reset
        self.loading_bar.hide()
        time.sleep(0.3)  # Wait for fade out to complete
        self.loading_bar.reset()

        # Deactivate loading state on icon/text (text reappears)
        self.send_icon_text.set_loading_state(False)

        # Finish loading
        self._is_loading = False
