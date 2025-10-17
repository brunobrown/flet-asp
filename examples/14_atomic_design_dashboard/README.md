# Example 14: Atomic Design Dashboard

A comprehensive dashboard application demonstrating how to build scalable design systems using the **Atomic Design methodology** with **flet-asp** for reactive state management.

## 🎯 What You'll Learn

- How to structure a Flet application using Atomic Design principles
- Building reusable component libraries from atoms to pages
- Integrating flet-asp reactive state with design systems
- Creating consistent, maintainable UI architectures
- Real-time data updates with reactive bindings

## 📁 Project Structure

```
14_atomic_design_dashboard/
├── __init__.py          # Package initialization
├── atoms.py             # Basic UI elements (buttons, text, inputs)
├── molecules.py         # Simple combinations (cards, menu items)
├── organisms.py         # Complex components (sidebar, tables)
├── templates.py         # Page layouts
├── pages.py             # Complete screens
├── main.py              # Application entry point
└── README.md            # This file
```

## 🔬 Atomic Design Hierarchy

### Level 1: Atoms (`atoms.py`)
Basic UI elements that cannot be broken down further:
- Text styles (heading1, heading2, body_text, caption_text)
- Buttons (primary_button, secondary_button, icon_button)
- Inputs (text_input, dropdown)
- Icons and dividers

**Example:**
```python
from atoms import heading1, primary_button

title = heading1("Dashboard")
button = primary_button("Save", on_click=save_handler)
```

### Level 2: Molecules (`molecules.py`)
Simple combinations of atoms that work as functional units:
- stat_card: Shows a metric with icon and value
- menu_item: Navigation item with icon and label
- form_field: Label + input combination
- search_bar: Icon + input field
- user_avatar: User initials in circular container

**Example:**
```python
from molecules import stat_card

card = stat_card(
    title="Total Users",
    value="1,234",
    icon_name=ft.Icons.PEOPLE,
    ref=user_count_ref  # Bound to state!
)
```

### Level 3: Organisms (`organisms.py`)
Complex components composed of molecules and atoms:
- sidebar: Complete navigation panel
- top_bar: Page header with search and actions
- stats_grid: Dashboard metrics overview (4 stat cards)
- data_table: Full table with headers, rows, and actions
- settings_form: Complete form with multiple fields

**Example:**
```python
from organisms import stats_grid

grid = stats_grid(
    total_users_ref=users_ref,
    revenue_ref=revenue_ref,
    orders_ref=orders_ref,
    growth_ref=growth_ref,
)
```

### Level 4: Templates (`templates.py`)
Page-level layouts that position organisms:
- dashboard_template: Sidebar + top bar + content area
- centered_content_template: Centered, constrained content
- full_width_template: Full-width content area

**Example:**
```python
from templates import dashboard_template

layout = dashboard_template(
    page=page,
    current_view="dashboard",
    title="Dashboard",
    content=main_content,
)
```

### Level 5: Pages (`pages.py`)
Complete screens with real content and state bindings:
- dashboard_page: Main metrics and recent orders
- analytics_page: Detailed analytics view
- users_page: User management
- orders_page: Order history
- settings_page: User settings with two-way binding
- help_page: Documentation and support

**Example:**
```python
from pages import dashboard_page

page_content = dashboard_page(
    page,
    total_users_ref,
    revenue_ref,
    orders_ref,
    growth_ref,
)
```

## 🔄 State Management Integration

This example demonstrates how flet-asp atoms bind seamlessly to the design system:

```python
# 1. Create state atoms
page.state.atom("total_users", "1,234")
page.state.atom("revenue", "$45,678")

# 2. Create refs for UI components
total_users_ref = ft.Ref[ft.Text]()
revenue_ref = ft.Ref[ft.Text]()

# 3. Bind state to UI (one-way)
page.state.bind("total_users", total_users_ref, prop="value")
page.state.bind("revenue", revenue_ref, prop="value")

# 4. Pass refs to organisms
stats_grid(
    total_users_ref=total_users_ref,
    revenue_ref=revenue_ref,
)

# 5. Update state = UI updates automatically!
page.state.set("total_users", "2,500")  # ✨ UI updates instantly
```

### Two-Way Binding in Forms

```python
# Settings form with two-way binding
page.state.atom("user_name", "Admin User")
name_ref = ft.Ref[ft.TextField]()

page.state.bind_two_way("user_name", name_ref, prop="value")

# Changes in UI → update state
# Changes in state → update UI
```

## 🚀 Running the Example

```bash
# From project root
python examples/14_atomic_design_dashboard/main.py

# Or as a module
python -m examples.14_atomic_design_dashboard.main
```

## ✨ Features

### 1. **Real-Time Updates**
Dashboard metrics update automatically every 5 seconds, demonstrating reactive state propagation through the component hierarchy.

### 2. **Navigation**
Click sidebar menu items to navigate between pages. State is preserved across navigation.

### 3. **Search Functionality**
Search bar in Users page demonstrates two-way binding with input controls.

### 4. **Responsive Layout**
Stats grid uses ResponsiveRow for mobile-friendly layouts.

### 5. **Reusable Components**
Every component can be reused across pages with different data and bindings.

## 🎨 Design System Benefits

### Consistency
All UI elements follow the same design language defined in atoms.

### Maintainability
Changes to atoms propagate throughout the entire application.

### Scalability
Easy to add new pages by combining existing organisms and templates.

### Testability
Individual atoms, molecules, and organisms can be tested in isolation.

### Collaboration
Designers and developers can work on different levels independently.

## 📚 Learn More

- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/)
- [Flet-ASP Documentation](https://github.com/brunobrown/flet-asp)
- [Building Design Systems](https://www.designbetter.co/design-systems-handbook)

## 🔧 Customization

### Adding a New Page

1. Create organism in `organisms.py` (if needed)
2. Create page function in `pages.py`
3. Add route in `main.py` `render_view()`
4. Add menu item in `organisms.py` sidebar

### Changing Theme

Modify color values in atoms:

```python
# atoms.py
def primary_button(text: str, on_click=None, **kwargs):
    return ft.ElevatedButton(
        text=text,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_700,  # Change primary color
        ),
        **kwargs
    )
```

### Adding State Atoms

```python
# main.py
page.state.atom("new_metric", "initial_value")
new_metric_ref = ft.Ref[ft.Text]()
page.state.bind("new_metric", new_metric_ref, prop="value")
```

## 💡 Best Practices

1. **Keep atoms simple** - One responsibility per component
2. **Use refs for state binding** - Connect UI to reactive state
3. **Compose up the hierarchy** - Build complex from simple
4. **Maintain consistency** - Use atoms for all text, buttons, etc.
5. **Document components** - Clear docstrings for each level

## 🐛 Troubleshooting

**Issue: Components not updating**
- Ensure refs are passed correctly through the hierarchy
- Check that state.bind() is called before page.add()

**Issue: Layout issues**
- Verify Container expand=True for flexible layouts
- Check ResponsiveRow columns configuration

**Issue: State not persisting**
- Ensure atoms are created before navigation
- Use page.state, not local StateManager instances