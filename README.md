<p align="center"><img src="https://github.com/user-attachments/assets/84c2835b-9356-42ae-8a78-7c3ac11679c1" width="25%" alt="flet-asp"></p>
<h1 align="center"> Flet ASP - Flet Atomic State Pattern</h1>

---

## 📖 Overview

**Flet ASP** (Flet Atomic State Pattern) is a reactive state management library for [Flet](https://flet.dev), bringing atom-based architecture and separation of concerns into Python apps — inspired by Flutter's [Riverpod](https://riverpod.dev) and [ASP](https://pub.dev/packages/asp).

It provides predictable, testable, and declarative state through:
- `Atom` – single reactive unit of state
- `Selector` – derived/computed state
- `Action` – handles async workflows like login, fetch, etc.

---

## 📦 Installation

Install using your package manager of choice:

```bash
# Pip
pip install flet-asp

# Poetry
poetry add flet-asp

# UV
uv add flet-asp
```

---

## ✨ Key Features

✅ **Reactive atoms** - Automatic UI updates when state changes  
✅ **Selectors** - Derived/computed state (sync & async)  
✅ **Actions** - Async-safe workflows for API calls, auth, etc.  
✅ **One-way & two-way binding** - Seamless form input synchronization  
✅ **Hybrid update strategy** - Bindings work even before controls are mounted  
✅ **Python 3.14+ optimizations** - Free-threading, incremental GC, 3-5% faster  
✅ **Lightweight** - No dependencies beyond Flet  
✅ **Type-safe** - Full type hints support

---

## 🚀 Quick Start

### 1. Basic Counter (Your First Atom)

The simplest way to use Flet-ASP: create an atom, bind it to a control, and update it.

```python
import flet as ft
import flet_asp as fa

def main(page: ft.Page):
    # Initialize state manager
    fa.get_state_manager(page)

    # Create a reactive atom
    page.state.atom("count", 0)

    # Create UI references
    count_text = ft.Ref[ft.Text]()

    def increment(e):
        # Update the atom - UI updates automatically!
        current = page.state.get("count")
        page.state.set("count", current + 1)

    # Build UI
    page.add(
        ft.Column([
            ft.Text("Counter", size=30),
            ft.Text(ref=count_text, size=50),
            ft.ElevatedButton("Increment", on_click=increment)
        ])
    )

    # Bind atom to UI - the Text will update automatically
    page.state.bind("count", count_text)

ft.app(target=main)
```

**What's happening here?**
1. `atom("count", 0)` - Creates a reactive piece of state
2. `bind("count", count_text)` - Connects state to UI
3. `set("count", value)` - Updates state → UI updates automatically!

---

### 2. Form with Two-Way Binding

Perfect for input fields that need to sync with state.

```python
import flet as ft
import flet_asp as fa

def main(page: ft.Page):
    fa.get_state_manager(page)

    # Create atoms for form fields
    page.state.atom("email", "")
    page.state.atom("password", "")

    # UI references
    email_field = ft.Ref[ft.TextField]()
    password_field = ft.Ref[ft.TextField]()
    message_text = ft.Ref[ft.Text]()

    def login(e):
        email = page.state.get("email")
        password = page.state.get("password")

        if email == "user@example.com" and password == "123":
            message_text.current.value = f"Welcome, {email}!"
        else:
            message_text.current.value = "Invalid credentials"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Login Form", size=24),
            ft.TextField(ref=email_field, label="Email"),
            ft.TextField(ref=password_field, label="Password", password=True),
            ft.ElevatedButton("Login", on_click=login),
            ft.Text(ref=message_text)
        ])
    )

    # Two-way binding: TextField ↔ Atom
    page.state.bind_two_way("email", email_field)
    page.state.bind_two_way("password", password_field)

ft.app(target=main)
```

**Key concept:** `bind_two_way()` keeps the TextField and atom in perfect sync!

---

### 3. Computed State with Selectors

Derive new values from existing state automatically.

```python
import flet as ft
import flet_asp as fa

def main(page: ft.Page):
    fa.get_state_manager(page)

    # Base atoms
    page.state.atom("first_name", "John")
    page.state.atom("last_name", "Doe")

    # Computed state - automatically recalculates when dependencies change
    @page.state.selector("full_name")
    def compute_full_name(get):
        return f"{get('first_name')} {get('last_name')}"

    # UI
    first_field = ft.Ref[ft.TextField]()
    last_field = ft.Ref[ft.TextField]()
    full_name_text = ft.Ref[ft.Text]()

    page.add(
        ft.Column([
            ft.Text("Name Builder", size=24),
            ft.TextField(ref=first_field, label="First Name"),
            ft.TextField(ref=last_field, label="Last Name"),
            ft.Divider(),
            ft.Text("Full Name:", weight=ft.FontWeight.BOLD),
            ft.Text(ref=full_name_text, size=20, color=ft.Colors.BLUE)
        ])
    )

    # Bind inputs
    page.state.bind_two_way("first_name", first_field)
    page.state.bind_two_way("last_name", last_field)

    # Bind computed state
    page.state.bind("full_name", full_name_text)

ft.app(target=main)
```

**Magic!** The full name updates automatically when first or last name changes.

---

### 4. Async Operations with Actions

Handle API calls, async operations, and side effects cleanly.

```python
import asyncio
import flet as ft
import flet_asp as fa

def main(page: ft.Page):
    fa.get_state_manager(page)

    page.state.atom("user", None)
    page.state.atom("loading", False)

    # Define async action
    async def login_action(get, set_value, params):
        set_value("loading", True)

        # Simulate API call
        await asyncio.sleep(2)

        # Validate credentials
        email = params.get("email")
        password = params.get("password")

        if email == "test@test.com" and password == "123":
            set_value("user", {"email": email, "name": "Test User"})
        else:
            set_value("user", None)

        set_value("loading", False)

    # Create action
    login = fa.Action(login_action)

    # UI
    email_field = ft.Ref[ft.TextField]()
    password_field = ft.Ref[ft.TextField]()
    status_text = ft.Ref[ft.Text]()

    async def handle_login(e):
        await login.run_async(
            page.state,
            {
                "email": email_field.current.value,
                "password": password_field.current.value
            }
        )

        user = page.state.get("user")
        if user:
            status_text.current.value = f"Welcome, {user['name']}!"
        else:
            status_text.current.value = "Login failed"
        page.update()

    # Listen to loading state
    def on_loading_change(is_loading):
        status_text.current.value = "Logging in..." if is_loading else ""
        page.update()

    page.state.listen("loading", on_loading_change)

    page.add(
        ft.Column([
            ft.Text("Async Login", size=24),
            ft.TextField(ref=email_field, label="Email"),
            ft.TextField(ref=password_field, label="Password", password=True),
            ft.ElevatedButton("Login", on_click=handle_login),
            ft.Text(ref=status_text)
        ])
    )

ft.app(target=main)
```

**Actions** encapsulate complex async logic in a testable, reusable way.

---

## 📚 Advanced Usage

### Custom Controls with Reactive State

Create reusable components with encapsulated state.

```python
import flet as ft
import flet_asp as fa

class Counter(ft.Column):
    """Reusable counter component with its own state."""

    def __init__(self, page: ft.Page, counter_id: str, title: str):
        super().__init__()
        self.page = page
        self.counter_id = counter_id
        self.value_text = ft.Ref[ft.Text]()

        # Initialize state for this counter
        page.state.atom(f"{counter_id}_count", 0)

        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(ref=self.value_text, size=40, color=ft.Colors.BLUE),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            on_click=self.decrement
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=self.increment
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                border=ft.border.all(2, ft.Colors.BLUE),
                border_radius=10
            )
        ]

    def did_mount(self):
        # Bind when component is mounted
        self.page.state.bind(f"{self.counter_id}_count", self.value_text)

    def increment(self, e):
        current = self.page.state.get(f"{self.counter_id}_count")
        self.page.state.set(f"{self.counter_id}_count", current + 1)

    def decrement(self, e):
        current = self.page.state.get(f"{self.counter_id}_count")
        self.page.state.set(f"{self.counter_id}_count", current - 1)

def main(page: ft.Page):
    fa.get_state_manager(page)

    page.add(
        ft.Column([
            ft.Text("Multiple Counters", size=30),
            ft.Row([
                Counter(page, "counter1", "Counter A"),
                Counter(page, "counter2", "Counter B"),
                Counter(page, "counter3", "Counter C")
            ])
        ])
    )

ft.app(target=main)
```

---

### Navigation with State Preservation

State persists across navigation automatically!

```python
import flet as ft
import flet_asp as fa

def home_screen(page: ft.Page):
    """Home screen with shared state."""
    count_text = ft.Ref[ft.Text]()

    def go_to_settings(e):
        page.views.clear()
        page.views.append(settings_screen(page))
        page.update()

    return ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.BLUE),
            ft.Column([
                ft.Text("Counter Value:", size=20),
                ft.Text(ref=count_text, size=50, color=ft.Colors.BLUE),
                ft.ElevatedButton("Go to Settings", on_click=go_to_settings)
            ])
        ]
    )

def settings_screen(page: ft.Page):
    """Settings screen - modifies shared state."""

    def increment(e):
        current = page.state.get("count")
        page.state.set("count", current + 1)

    def go_back(e):
        page.views.clear()
        page.views.append(home_screen(page))
        page.update()

    return ft.View(
        "/settings",
        [
            ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.Colors.GREEN),
            ft.Column([
                ft.Text("Modify Counter", size=20),
                ft.ElevatedButton("Increment", on_click=increment),
                ft.ElevatedButton("Go Back", on_click=go_back)
            ])
        ]
    )

def main(page: ft.Page):
    fa.get_state_manager(page)

    # Shared state across screens
    page.state.atom("count", 0)

    page.views.append(home_screen(page))

    # Bind state after adding view (works with hybrid strategy!)
    count_ref = page.views[0].controls[1].controls[1]  # Get the count text
    page.state.bind("count", ft.Ref[ft.Text]())

ft.app(target=main)
```

---

### Global State Outside Page Scope

For advanced scenarios like testing, multi-window applications, or complex state architectures, you can create a `StateManager` **outside** the page scope.

```python
import flet as ft
import flet_asp as fa

# Create global StateManager OUTSIDE the page
global_state = fa.StateManager()

def screen_a(page: ft.Page):
    """Main screen with counter."""
    count_ref = ft.Ref[ft.Text]()

    def increment(e):
        # Use global_state instead of page.state
        global_state.set("count", global_state.get("count") + 1)

    def go_to_b(e):
        page.go("/b")

    view = ft.View(
        "/",
        [
            ft.Text("Screen A - Global State", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(ref=count_ref, size=40, color=ft.Colors.BLUE_700),
            ft.ElevatedButton("Increment", on_click=increment),
            ft.ElevatedButton("Go to Screen B", on_click=go_to_b),
        ],
        padding=20,
    )

    # Bind using global_state
    global_state.bind("count", count_ref)
    return view

def screen_b(page: ft.Page):
    """Secondary screen displaying the counter."""
    def go_back(e):
        page.go("/")

    return ft.View(
        "/b",
        [
            ft.Text("Screen B - Global State", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Counter value: {global_state.get('count')}", size=16),
            ft.Text("State is managed globally!", color=ft.Colors.GREEN_700),
            ft.ElevatedButton("Go back", on_click=go_back),
        ],
        padding=20,
    )

def main(page: ft.Page):
    """App entry point."""
    # IMPORTANT: Attach the page to the global StateManager
    global_state.page = page

    # Initialize atoms
    global_state.atom("count", 0)

    def route_change(e):
        page.views.clear()
        if page.route == "/b":
            page.views.append(screen_b(page))
        else:
            page.views.append(screen_a(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
```

**When to use global state:**

| Use Case | Why Global State? |
|----------|-------------------|
| **Unit Testing** | Test state logic without creating a Flet page |
| **Multi-Window Apps** | Share state between multiple page instances |
| **Advanced Architectures** | State exists independently of UI lifecycle |
| **Framework Integration** | Flet-ASP as part of a larger system |

**Key differences:**

| Aspect | `page.state` | `global_state` |
|--------|--------------|----------------|
| **Creation** | `fa.get_state_manager(page)` | `fa.StateManager()` |
| **Page binding** | Automatic | Manual (`global_state.page = page`) |
| **Scope** | Inside `main()` | Global (module level) |
| **Lifecycle** | Managed by page | Manual |
| **When to use** | ✅ Most cases | ⚠️ Specific scenarios |

**Common pitfalls:**

```python
# ❌ WRONG - Forgot to attach page
global_state = fa.StateManager()

def main(page: ft.Page):
    global_state.atom("count", 0)  # Error: page not attached!

# ✅ CORRECT - Attach page first
global_state = fa.StateManager()

def main(page: ft.Page):
    global_state.page = page  # Attach first!
    global_state.atom("count", 0)
```

**Testing example:**

```python
import unittest
import flet_asp as fa

# Global state for testing
test_state = fa.StateManager()

class TestMyLogic(unittest.TestCase):
    def setUp(self):
        test_state._atoms.clear()
        test_state.atom("count", 0)

    def test_increment(self):
        # Test logic without creating a Flet page
        test_state.set("count", test_state.get("count") + 1)
        self.assertEqual(test_state.get("count"), 1)

    def test_computed_value(self):
        test_state.atom("double", lambda: test_state.get("count") * 2)
        test_state.set("count", 5)
        self.assertEqual(test_state.get("double"), 10)
```

For a complete example, see [`11.1_global_state_outside.py`](./examples/11.1_global_state_outside.py).

---

### Complex Selectors with Async Data

Fetch and compute data asynchronously.

```python
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
            3: {"name": "Charlie", "email": "charlie@example.com"}
        }

        return users.get(user_id, {"name": "Unknown", "email": "N/A"})

    # UI
    user_info = ft.Ref[ft.Text]()

    def update_user_info(user_data):
        # Async selectors may return coroutines on first call, check the type
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
        ft.Column([
            ft.Text("User Profile", size=24),
            ft.Text(ref=user_info, size=18),
            ft.ElevatedButton("Next User", on_click=next_user)
        ])
    )

ft.app(target=main)
```

---

### Shopping Cart Example

Real-world e-commerce state management.

```python
import flet as ft
import flet_asp as fa

def main(page: ft.Page):
    fa.get_state_manager(page)

    # State
    page.state.atom("cart_items", [])

    # Selectors
    @page.state.selector("cart_total")
    def calculate_total(get):
        items = get("cart_items")
        return sum(item["price"] * item["quantity"] for item in items)

    @page.state.selector("cart_count")
    def count_items(get):
        items = get("cart_items")
        return sum(item["quantity"] for item in items)

    # Available products
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Mouse", "price": 29.99},
        {"id": 3, "name": "Keyboard", "price": 79.99}
    ]

    # UI refs
    cart_list = ft.Ref[ft.Column]()
    cart_count_text = ft.Ref[ft.Text]()
    cart_total_text = ft.Ref[ft.Text]()

    def add_to_cart(product):
        items = page.state.get("cart_items")

        # Check if item already in cart
        existing = next((item for item in items if item["id"] == product["id"]), None)

        if existing:
            existing["quantity"] += 1
        else:
            items.append({**product, "quantity": 1})

        page.state.set("cart_items", items)

    def render_cart():
        items = page.state.get("cart_items")

        cart_list.current.controls = [
            ft.ListTile(
                title=ft.Text(item["name"]),
                subtitle=ft.Text(f"${item['price']:.2f} × {item['quantity']}"),
                trailing=ft.Text(f"${item['price'] * item['quantity']:.2f}")
            ) for item in items
        ] if items else [ft.Text("Cart is empty")]

        page.update()

    # Listen to cart changes
    page.state.listen("cart_items", lambda _: render_cart())

    # Build UI
    page.add(
        ft.Row([
            # Products column
            ft.Column([
                ft.Text("Products", size=24),
                *[
                    ft.ElevatedButton(
                        f"{p['name']} - ${p['price']:.2f}",
                        on_click=lambda e, product=p: add_to_cart(product)
                    ) for p in products
                ]
            ], expand=1),

            # Cart column
            ft.Column([
                ft.Text("Shopping Cart", size=24),
                ft.Text(ref=cart_count_text),
                ft.Column(ref=cart_list),
                ft.Divider(),
                ft.Text(ref=cart_total_text, size=20, weight=ft.FontWeight.BOLD)
            ], expand=1)
        ])
    )

    # Bind computed values
    page.state.bind("cart_count", cart_count_text, prop="value")
    page.state.bind("cart_total", cart_total_text, prop="value")

    render_cart()

ft.app(target=main)
```

---

## ⚡ Performance & Python 3.14+

**Flet-ASP** includes a **hybrid update strategy** that ensures bindings work reliably, even when controls are bound before being added to the page.

### Hybrid Strategy:
1. **Lazy updates** - Property is always set (never fails)
2. **Immediate updates** - Tries to update if control is mounted (99% of cases)
3. **Lifecycle hooks** - Hooks into `did_mount` for custom controls
4. **Queue fallback** - Retries when `page.update()` is called

### Python 3.14+ Optimizations:

| Feature | Benefit | Performance Gain |
|---------|---------|------------------|
| **Free-threading** | Process bindings in parallel without GIL | Up to 4x faster for large apps |
| **Incremental GC** | Smaller garbage collection pauses | 10x smaller pauses (20ms → 2ms) |
| **Tail call interpreter** | Faster Python execution | 3-5% overall speedup |

**Configuration** (optional):
```python
from flet_asp.atom import Atom

# For giant apps with 1000+ bindings on Python 3.14+
Atom.MAX_PARALLEL_BINDS = 8

# For small apps or to disable free-threading
Atom.ENABLE_FREE_THREADING = False
```

For more details, see [PERFORMANCE.md](./PERFORMANCE.md).

---

## 📁 More Examples

Explore the [`examples/`](./examples/) folder for complete applications:

**Basic Examples:**
- [`1.0_counter_atom.py`](./examples/1.0_counter_atom.py) - Simple counter
- [`1.1_counter_atom_using_state_alias.py`](./examples/1.1_counter_atom_using_state_alias.py) - Counter with page.state
- [`2_counter_atom_bind_dynamic.py`](./examples/2_counter_atom_bind_dynamic.py) - Dynamic binding

**Intermediate Examples:**
- [`3_computed_fullname.py`](./examples/3_computed_fullname.py) - Computed state
- [`4_action_login.py`](./examples/4_action_login.py) - Async actions
- [`5_selector_user_email.py`](./examples/5_selector_user_email.py) - Selectors
- [`6_listen_user_login.py`](./examples/6_listen_user_login.py) - State listeners
- [`7_bind_two_way_textfield.py`](./examples/7_bind_two_way_textfield.py) - Two-way binding
- [`8_session_reset_clear.py`](./examples/8_session_reset_clear.py) - State cleanup

**Advanced Examples:**
- [`9_todo.py`](./examples/9_todo.py) - Complete ToDo app
- [`10_cart_app.py`](./examples/10_cart_app.py) - Shopping cart
- [`11_screen_a_navigation_screen_b.py`](./examples/11_screen_a_navigation_screen_b.py) - Navigation with page.state
- [`11.1_global_state_outside.py`](./examples/11.1_global_state_outside.py) - Global state outside page scope
- [`12_python314_performance.py`](./examples/12_python314_performance.py) - Performance demo
- [`13_hybrid_binding_advanced.py`](./examples/13_hybrid_binding_advanced.py) - Hybrid binding

**Atomic Design Examples:**
- [`14_atomic_design_dashboard/`](./examples/14_atomic_design_dashboard/) - Complete dashboard with atoms, molecules, organisms, templates, and pages
- [`15_atomic_design_theming/`](./examples/15_atomic_design_theming/) - Theme-aware component library with design tokens
- [`16_reactive_atomic_components/`](./examples/16_reactive_atomic_components/) - Reactive components with built-in state management

---

## 🧩 Building Design Systems with Atomic Design
<p align="center">
    <img src="https://github.com/user-attachments/assets/2d31c317-8b76-4d4d-8d9b-ab64da600ddd" alt="Atomic Design System" width="100%">
</p>

**Flet-ASP** is designed from the ground up to work seamlessly with the **Atomic Design methodology** - a powerful approach for building scalable, maintainable design systems.

### What is Atomic Design?

Atomic Design is a methodology for creating design systems by breaking down interfaces into fundamental building blocks, inspired by chemistry:

**🔬 Atoms** → **🧪 Molecules** → **🧬 Organisms** → **📄 Templates** → **📱 Pages**

### How Flet-ASP Maps to Atomic Design

| Atomic Design Layer | Flet-ASP Feature | Example |
|---------------------|------------------|---------|
| **Atoms** | Reactive state values | `page.state.atom("email", "")` |
| **Molecules** | Computed state | `@page.state.selector("full_name")` |
| **Organisms** | Actions & workflows | `Action(login_function)` |
| **Templates** | State bindings | `page.state.bind("count", ref)` |
| **Pages** | Complete screens | Custom controls with encapsulated state |

### Real-World Atomic Design with Flet-ASP

We provide **two comprehensive examples** that demonstrate professional design system architecture:

#### 📊 Example 14: Dashboard Design System

A complete dashboard application showcasing the full Atomic Design hierarchy:

- **Atoms**: Buttons, inputs, text styles, icons, dividers
- **Molecules**: Stat cards, menu items, form fields, search bars
- **Organisms**: Sidebar, top bar, data tables, stats grid
- **Templates**: Dashboard layouts with different content arrangements
- **Pages**: Dashboard, analytics, users, orders, settings screens

```python
# Atoms define the foundation
from atoms import heading1, primary_button

# Molecules combine atoms
from molecules import stat_card

# Organisms compose molecules
from organisms import stats_grid

# Templates arrange organisms
from templates import dashboard_template

# Pages bring it all together
from pages import dashboard_page
```

**Features:**
- ✅ Complete component hierarchy following Atomic Design
- ✅ Real-time data updates with reactive state bindings
- ✅ Navigation with state preservation
- ✅ Reusable components across multiple pages
- ✅ Consistent design language

[**View Example →**](./examples/14_atomic_design_dashboard/)

#### 🎨 Example 15: Theme-Aware Component Library

An advanced example demonstrating **design tokens** and dynamic theming:

- **Design Tokens**: Colors, typography, spacing, border radius
- **Theme-Aware Atoms**: Components that adapt to light/dark modes
- **Reactive Theming**: Real-time theme switching with flet-asp
- **Semantic Colors**: Success, warning, error, info states

```python
from theme_tokens import get_theme
from atoms import filled_button, text_field
from molecules import alert, stat_card

# All components automatically adapt to current theme
theme = get_theme()
button = filled_button("Submit")  # Uses theme.colors.primary
```

**Features:**
- ✅ Complete design token system (colors, typography, spacing)
- ✅ Light and dark mode support
- ✅ Theme switching without page reload
- ✅ Semantic color system for alerts and states
- ✅ Professional design system architecture

[**View Example →**](./examples/15_atomic_design_theming/)

#### ⚛️ Example 16: Reactive Atomic Components

Components that **combine visual structure + reactive state** in a single, reusable package:

```python
from reactive_atoms import ReactiveCounter, ReactiveStatCard, ReactiveForm

# Create counter with built-in state!
counter = ReactiveCounter(page, "Counter A", initial_count=0)
page.add(counter.control)

# Interact via clean API
counter.increment()  # +1
counter.decrement()  # -1
counter.reset()      # Set to 0
print(counter.value) # Get current value

# Stat card with auto-updates
users_card = ReactiveStatCard(
    page,
    title="Total Users",
    atom_key="users",
    initial_value="1,234",
    icon_name=ft.Icons.PEOPLE,
    show_trend=True
)

# Update programmatically
users_card.update_with_trend("2,500", "+15%")  # ✨ UI updates automatically!
```

**Features:**
- ✅ Components with built-in reactive state
- ✅ No manual binding needed
- ✅ Clean, intuitive API
- ✅ Encapsulated state management
- ✅ Reusable across projects

[**View Example →**](./examples/16_reactive_atomic_components/)

### Why Atomic Design + Flet-ASP?

**🎯 Consistency**: Design tokens and atoms ensure uniform styling across your app

**🔄 Reusability**: Build components once, use them everywhere with different state bindings

**📈 Scalability**: Add new features by combining existing atoms and molecules

**🧪 Testability**: Test atoms, molecules, and organisms in isolation

**🤝 Collaboration**: Designers and developers work with the same component language

**⚡ Reactivity**: State changes propagate automatically through the component hierarchy

### Learn More About Atomic Design

- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/) - The definitive guide
- [Building Design Systems with Atomic Design](https://www.designbetter.co/design-systems-handbook)
- [Material Design System](https://m3.material.io/) - Real-world example
- [Flet-ASP Examples](./examples/) - Practical implementations

---

## 🌐 Community

Join the community to contribute or get help:

- [Discord](https://discord.gg/dzWXP8SHG8)
- [GitHub Issues](https://github.com/brunobrown/flet-asp/issues)

## ⭐ Support

If you like this project, please give it a [GitHub star](https://github.com/brunobrown/flet-asp) ⭐

---

## 🤝 Contributing

Contributions and feedback are welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed explanation

For feedback, [open an issue](https://github.com/brunobrown/flet-asp/issues) with your suggestions.

---

<p align="center"><img src="https://github.com/user-attachments/assets/431aa05f-5fbc-4daa-9689-b9723583e25a" width="50%"></p>
<p align="center"><a href="https://www.bible.com/bible/116/PRO.16.NLT"> Commit your work to the LORD, and your plans will succeed. Proverbs 16:3</a></p>
