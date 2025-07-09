import flet as ft
import fasp as fa
from typing import Callable


class TaskItem(ft.Column):
    """
    A reusable UI component representing a task row,
    in edit or display mode based on the `editing` flag.
    """

    def __init__(
            self,
            task_data: dict,
            on_toggle: Callable,
            on_delete: Callable,
            on_edit: Callable,
            on_save: Callable,
    ):
        super().__init__()
        self.task_data = task_data
        self.title_ref = ft.Ref[ft.TextField]()

        if task_data.get("editing", False):
            self.controls = [ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.TextField(
                        ref=self.title_ref,
                        value=task_data["title"],
                        border=ft.InputBorder.UNDERLINE,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.Colors.GREEN,
                        tooltip="Save task",
                        on_click=lambda e: on_save(task_data["id"], self.title_ref.current.value)
                    )
                ]
            )]
        else:
            self.controls = [ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Checkbox(
                        value=task_data["completed"],
                        label=task_data["title"],
                        on_change=lambda e: on_toggle(task_data["id"]),
                    ),
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CREATE_OUTLINED,
                                tooltip="Edit task",
                                on_click=lambda e: on_edit(task_data["id"]),
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                tooltip="Delete task",
                                on_click=lambda e: on_delete(task_data["id"]),
                            ),
                        ],
                    ),
                ],
            )]


def main(page: ft.Page):
    """
        This example demonstrates a complete ToDo application using FASP with full reactivity. It manages tasks using:
            * atom() for reactive task list and inputs
            * selector() to derive the count of active tasks
            * Action to clear completed tasks
            * listen() to update the UI based on filter changes and task mutations

        The app supports:
            * Adding, editing, and deleting tasks
            * Filtering by all, active, or completed
            * Persisted updates using centralized FASP state
        """

    state = fa.get_state_manager(page)

    # Declare reactive atoms
    state.atom("tasks", [])
    state.atom("new_task", "")
    state.atom("filter", "all")

    # UI references
    input_ref = ft.Ref[ft.TextField]()
    tasks_column_ref = ft.Ref[ft.Column]()
    tabs_ref = ft.Ref[ft.Tabs]()
    active_count_ref = ft.Ref[ft.Text]()

    # Task logic
    def add_task(e):
        title = state.get("new_task").strip()
        if not title:
            return
        tasks = state.get("tasks")
        new_id = max([t["id"] for t in tasks], default=0) + 1
        tasks.append({"id": new_id, "title": title, "completed": False, "editing": False})
        state.set("tasks", tasks)
        state.set("new_task", "")

    def toggle_task(task_id: int):
        tasks = state.get("tasks")
        for t in tasks:
            if t["id"] == task_id:
                t["completed"] = not t["completed"]
        state.set("tasks", tasks)

    def delete_task(task_id: int):
        tasks = [t for t in state.get("tasks") if t["id"] != task_id]
        state.set("tasks", tasks)

    def edit_task(task_id: int):
        tasks = state.get("tasks")
        for t in tasks:
            t["editing"] = (t["id"] == task_id)
        state.set("tasks", tasks)

    def save_task(task_id: int, new_title: str):
        tasks = state.get("tasks")
        for t in tasks:
            if t["id"] == task_id:
                t["title"] = new_title
            t["editing"] = False
        state.set("tasks", tasks)

    def on_tab_change(e):
        tab_text = e.control.tabs[e.control.selected_index].text
        state.set("filter", tab_text)

    def render_tasks(_=None):
        tasks = state.get("tasks")
        current_filter = state.get("filter")

        if current_filter == "all":
            filtered = tasks
        elif current_filter == "active":
            filtered = [t for t in tasks if not t["completed"]]
        elif current_filter == "completed":
            filtered = [t for t in tasks if t["completed"]]
        else:
            filtered = tasks

        tasks_column_ref.current.controls = [
            TaskItem(
                t,
                toggle_task,
                delete_task,
                edit_task,
                save_task
            ) for t in filtered
        ]
        tasks_column_ref.current.update()

    # ✅ Selector: count active tasks
    @state.selector("active_count")
    def count_active(get):
        return len([t for t in get("tasks") if not t["completed"]])

    # Action: clear completed tasks
    async def clear_completed(get, set_value, _):
        set_value("tasks", [t for t in get("tasks") if not t["completed"]])

    clear_completed_action = fa.Action(clear_completed)

    # UI layout
    page.title = "ToDo App (FASP)"
    page.add(
        ft.Column([
            ft.Text("📋 ToDo with FASP", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Row([
                ft.TextField(
                    ref=input_ref,
                    expand=True,
                    hint_text="What needs to be done?",
                    on_change=lambda e: state.set("new_task", e.control.value)
                ),
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_task)
            ]),
            ft.Tabs(
                ref=tabs_ref,
                on_change=on_tab_change,
                selected_index=0,
                tabs=[
                    ft.Tab(text="all"),
                    ft.Tab(text="active"),
                    ft.Tab(text="completed"),
                ]
            ),
            ft.Row([
                ft.Text("Active tasks:"),
                ft.Text(ref=active_count_ref)
            ]),
            ft.Column(ref=tasks_column_ref, spacing=5),
            ft.OutlinedButton(
                text="Clear completed",
                on_click=lambda e: page.run_task(clear_completed_action.run_async, state)
            )
        ], width=600)
    )

    # Bindings
    state.bind("active_count", active_count_ref, prop="value")

    # Listeners
    state.listen("tasks", render_tasks)
    state.listen("filter", render_tasks)


if __name__ == "__main__":
    ft.app(target=main)
