<p align="center"><img src="https://github.com/user-attachments/assets/84c2835b-9356-42ae-8a78-7c3ac11679c1" width="25%" alt="flet-asp"></p>
<h1 align="center"> Flet ASP - Flet Atomic State Pattern</h1>

---

## 📖 Overview

**Flet ASP** (Flet Atomic State Pattern) is a reactive state management library for [Flet](https://flet.dev), bringing atom-based architecture and separation of concerns into Python apps — inspired by Flutter's [Riverpod](https://riverpod.dev) and [ASP](https://pub.dev/packages/asp).

It provides predictable, testable, and declarative state through:
- `Atom` – single reactive unit of state
- `Selector` – derived/computed state
- `Action` – handles async workflows like login, fetch, etc.

## 📦 Installation

Install using your package manager of choice:

**Pip**

```bash
pip install flet-asp
```

**Poetry**

```bash
poetry add flet-asp
```

**UV**

```bash
uv add flet-asp
```

---

## 📦 Features

✅ Reactive atoms (with controlled mutation)  
✅ Selector (sync & async derived values)  
✅ Async-safe Actions  
✅ One-way and two-way binding (form inputs)  
✅ Lightweight and framework-agnostic  
✅ Built for [Flet](https://flet.dev)

---

## 🧪 Example 1 – Basic Counter

```python
import flet as ft
import flet-asp as fa


def main(page: ft.Page):
    state = fa.get_state_manager(page)
    state.atom("count", 0)

    count_ref = ft.Ref[ft.Text]()

    def increment(e):
        state.set("count", state.get("count") + 1)

    page.add(
        ft.Text(ref=count_ref),
        ft.ElevatedButton("Increment", on_click=increment)
    )

    state.bind("count", count_ref)


if __name__ == "__main__":
    ft.app(target=main)

```

## 🧪 Example 2 – Basic counter using state alias

```python
import flet as ft
import flet-asp as fa


def main(page: ft.Page):
    fa.get_state_manager(page)
    page.state.atom("count", 0)

    count_ref = ft.Ref[ft.Text]()

    def increment(e):
        page.state.set("count", page.state.get("count") + 1)

    page.add(
        ft.Text(ref=count_ref),
        ft.ElevatedButton("Increment", on_click=increment)
    )

    page.state.bind("count", count_ref)


if __name__ == "__main__":
    ft.app(target=main)

```

---

## 📁 Examples Included

Explore the [`examples/`](./examples/) folder for full apps:

- [`1.0_counter_atom/`](./examples/1.0_counter_atom.py)
- [`1.1_counter_atom_using_state_alias/`](./examples/1.1_counter_atom_using_state_alias.py)
- [`2_counter_atom_bind_dynamic/`](./examples/2_counter_atom_bind_dynamic.py)
- [`3_computed_fullname/`](./examples/3_computed_fullname.py)
- [`4_action_login/`](./examples/4_action_login.py)
- [`5_selector_user_email/`](./examples/5_selector_user_email.py)
- [`6_listen_user_login/`](./examples/6_listen_user_login.py)
- [`7_bind_two_way_textfield/`](./examples/7_bind_two_way_textfield.py)
- [`8_session_reset_clear/`](./examples/8_session_reset_clear.py)
- [`9_todo/`](./examples/9_todo.py)
- [`10_cart_app/`](./examples/10_cart_app.py)

---

## 🧩 Design System Ready
<!--<p align="center"><img src="https://github.com/user-attachments/assets/1c620722-4f3f-4900-948b-aec59999f955" width="1000" height="200" alt="atomic_design"/></p>-->
<p align="center"><img src="https://github.com/user-attachments/assets/fef1f45c-31bb-4c6f-a944-5d60f0b0b259" width="1000" height="200" alt="atomic_design"/></p>

**Flet-ASP** also allows you to create applications following the `Atomic Design System`, just like Flutter.

| Atomic Layer | How Flet-ASP Helps                                                                                       |
|--------------|------------------------------------------------------------------------------------------------------|
| **Atoms**    | Simple reactive values (e.g., `atom("email")`, `atom("count")`, `atom("message")`, `atom("loading")` |
| **Selectors**| Derived state (e.g., `@selector("full_name")`, `@selector("total_price")` or `Selector(...)`)        |
| **Actions**  | Encapsulate side effects (API, auth)                                                                 |
| **Bindings** | `bind()`, `bind_two_way()` for full UI ↔ state reactivity                                            |
| **Molecules/Organisms** | Combine logic in components                                                               |
| **Templates** | Reuse UIs across screens                                                                            |

>Learn more:
> - [Atomic Design with Flutter](https://medium.com/@hlfdev/building-a-design-system-with-atomic-design-in-flutter-a7a16e28739b)
> - [Widget Componentization (pt-BR)](https://medium.com/mesainc/componentiza%C3%A7%C3%A3o-de-widgets-no-flutter-com-atomic-design-b8653fd2dc2b)

---

## 🌐 Community

#### Join the community to contribute or get help:

1. [Discord](https://discord.gg/dzWXP8SHG8)
2. [Report an issue](https://github.com/brunobrown/flet-asp/issues)

## ⭐ Support

If you like this project, please give it a [GitHub star](https://github.com/brunobrown/flet-asp) and stay tuned for future updates!

## 🤝🏽 Contributing

Contributions and feedback are welcome!

#### 🔧 How to contribute:

1. **Fork the repository.**
2. **Create a feature branch.**
3. **Submit a pull request with a detailed explanation of your changes.**

#### 💬 How to give feedback:

> We value your opinion! Feel free to share suggestions, ideas, or constructive criticism to help improve the project.

1. **Open an issue.**
2. **Describe the problem or suggestion clearly**
3. **Optionally propose a solution**

#### 🕓 Waiting for help?

Be patient — or reach out to the community on [Discord](https://discord.gg/dzWXP8SHG8) for quicker responses.

---

<p align="center"><img src="https://github.com/user-attachments/assets/431aa05f-5fbc-4daa-9689-b9723583e25a" width="50%"></p>

> [Commit your work to the LORD, and your plans will succeed. Proverbs 16: 3](https://www.bible.com/bible/116/PRO.16.NLT)
