import asyncio
import flet as ft
import flet_asp as fa


def main(page: ft.Page):
    fa.get_state_manager(page)

    # Base atoms
    page.state.atom("user_id", 1)

    # Async selector - fetches user data
    @page.state.selector("user_data")
    async def fetch_user(get):
        user_id = get("user_id")

        # Simulate API call
        await asyncio.sleep(1)

        # Mock user data
        users = {
            1: {"name": "Alice", "email": "alice@example.com"},
            2: {"name": "Bob", "email": "bob@example.com"},
            3: {"name": "Charlie", "email": "charlie@example.com"},
        }

        return users.get(user_id, {"name": "Unknown", "email": "N/A"})

    # UI
    user_info = ft.Ref[ft.Text]()

    def update_user_info(user_data):
        # Async selectors may return coroutines, check the type
        import inspect

        if inspect.iscoroutine(user_data):
            # Skip coroutine objects - they will be resolved automatically
            return
        if user_data:
            user_info.current.value = f"{user_data['name']} ({user_data['email']})"
        else:
            user_info.current.value = "Loading..."
        page.update()

    def next_user(e):
        current_id = page.state.get("user_id")
        page.state.set("user_id", (current_id % 3) + 1)

    # Listen to selector changes
    page.state.listen("user_data", update_user_info)

    page.add(
        ft.Column(
            [
                ft.Text("User Profile", size=24),
                ft.Text(ref=user_info, size=18),
                ft.ElevatedButton("Next User", on_click=next_user),
            ]
        )
    )


ft.app(target=main)
