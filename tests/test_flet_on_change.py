"""
Test to understand how Flet handles on_change
"""
import flet as ft


def main(page: ft.Page):
    page.title = "Test Flet on_change"

    def my_handler(e):
        print(f"my_handler called! e.data={e.data}")

    # Create TextField
    field = ft.TextField(label="Test")

    # Add to page FIRST
    page.add(field)

    print(f"After page.add, field.on_change = {field.on_change}")

    # NOW set on_change
    field.on_change = my_handler

    print(f"After setting, field.on_change = {field.on_change}")

    # Check after a delay
    import threading
    import time

    def check():
        time.sleep(1)
        print(f"\n[1s later] field.on_change = {field.on_change}")
        time.sleep(2)
        print(f"[3s later] field.on_change = {field.on_change}")
        print("\nNow type something...")

    threading.Thread(target=check, daemon=True).start()


if __name__ == "__main__":
    ft.app(target=main)
