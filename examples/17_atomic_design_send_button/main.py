"""
Example of AnimatedSendButton usage following the Atomic Design pattern with Flet-ASP.

Structure:
- components/atoms.py: Basic components (send_icon, button_text, cloud_icon, button_container)
- components/molecules.py: Atom combinations (SendIconWithText, CloudPair)
- components/organisms.py: Complex components (AnimatedSendButton)

Uses:
- flet_asp reactive state (atom, bind, selector)
- Flet lifecycle (build, did_mount, will_unmount)
"""

import flet as ft
import flet_asp as fa
from organisms import AnimatedSendButton


def main(page: ft.Page):
    # Initialize the reactive state manager
    fa.get_state_manager(page)

    # Configure page alignment
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Create the animated button using the organism (custom control)
    # Animations start automatically via did_mount()
    send_button = AnimatedSendButton(
        width=130,
        height=45,
        bgcolor=ft.Colors.BLUE_700,
        text_value="SEND",
        float_interval=0.5,
    )

    page.add(send_button)


if __name__ == "__main__":
    ft.app(target=main)
