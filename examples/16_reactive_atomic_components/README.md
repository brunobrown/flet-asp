# Example 16: Reactive Atomic Components

The ultimate combination of **Atomic Design** (visual structure) and **Flet-ASP** (reactive state) in a single component!

## 🎯 What You'll Learn

- Creating components with built-in reactive state
- Encapsulating state management within components
- Building reusable components with clean APIs
- Automatic binding and updates
- Component composition with reactive state

## 💡 The Big Idea

Instead of creating visual components separately and then manually binding them to state:

```python
# ❌ Old way - Manual binding
counter_text = ft.Ref[ft.Text]()
page.state.atom("count", 0)
page.add(ft.Text(ref=counter_text, size=50))
page.state.bind("count", counter_text)
```

Reactive components combine everything into one:

```python
# ✅ New way - Reactive component
counter = ReactiveCounter(page, "My Counter", initial_count=0)
page.add(counter.control)
# That's it! State, UI, and binding all included!
```

## 📁 Project Structure

```
16_reactive_atomic_components/
├── __init__.py          # Package documentation
├── reactive_atoms.py    # Reactive component library
├── main.py              # Demo application
└── README.md            # This file
```

## 🧩 Available Components

### ReactiveAtom (Base Class)

All reactive components inherit from this base class:

```python
class ReactiveAtom:
    def __init__(self, page, atom_key)
    def set(self, value)         # Update atom value
    def get(self)                # Get current value
    def listen(self, callback)   # Listen to changes
```

### 1. ReactiveText

Text that automatically updates when state changes:

```python
from reactive_atoms import ReactiveText

# Create reactive text
display = ReactiveText(
    page,
    atom_key="message",
    initial_value="Hello",
    size=24,
    color=ft.Colors.BLUE
)

page.add(display.control)

# Update anywhere
display.set("New message!")  # ✨ UI updates automatically
```

### 2. ReactiveCounter

Complete counter with increment/decrement/reset:

```python
from reactive_atoms import ReactiveCounter

counter = ReactiveCounter(
    page,
    title="Counter A",
    initial_count=0,
    step=1,
    color=ft.Colors.BLUE_700
)

page.add(counter.control)

# Interact programmatically
counter.increment()  # +1
counter.decrement()  # -1
counter.reset()      # Set to 0
print(counter.value) # Get current value
```

**Features:**
- ✅ Increment/decrement buttons
- ✅ Reset button
- ✅ Custom step size
- ✅ Custom colors
- ✅ Automatic UI updates

### 3. ReactiveStatCard

Dashboard metric card with trends:

```python
from reactive_atoms import ReactiveStatCard

users_card = ReactiveStatCard(
    page,
    title="Total Users",
    atom_key="total_users",
    initial_value="1,234",
    icon_name=ft.Icons.PEOPLE,
    color=ft.Colors.BLUE_700,
    show_trend=True
)

page.add(users_card.control)

# Update with trend
users_card.update_with_trend("2,500", "+15%")
```

**Perfect for:**
- 📊 Real-time dashboards
- 📈 Analytics displays
- 💰 Financial metrics
- 👥 User statistics

### 4. ReactiveInput

Input field with two-way reactive binding:

```python
from reactive_atoms import ReactiveInput

username = ReactiveInput(
    page,
    atom_key="username",
    initial_value="",
    label="Username",
    hint="Enter username"
)

page.add(username.control)

# Get value
print(username.get())  # Current input value

# Set value programmatically
username.set("JohnDoe")  # ✨ Field updates automatically
```

**Features:**
- ✅ Two-way binding (field ↔ state)
- ✅ Password mode support
- ✅ Validation ready
- ✅ Custom styling

### 5. ReactiveForm

Complete form with multiple fields:

```python
from reactive_atoms import ReactiveForm

def on_submit(data):
    print(f"Name: {data['name']}")
    print(f"Email: {data['email']}")

form = ReactiveForm(
    page,
    form_id="registration",
    title="User Registration",
    fields=[
        {"key": "name", "label": "Full Name", "hint": "Enter name"},
        {"key": "email", "label": "Email", "hint": "your@email.com"},
        {"key": "password", "label": "Password", "password": True}
    ],
    on_submit=on_submit
)

page.add(form.control)

# Access individual fields
name_field = form.get_field("name")
print(name_field.get())

# Reset form
form.reset()
```

**Features:**
- ✅ Multiple reactive inputs
- ✅ Built-in submit handler
- ✅ Field access by key
- ✅ Form reset functionality

### 6. ReactiveProgress

Progress bar with automatic percentage calculation:

```python
from reactive_atoms import ReactiveProgress

progress = ReactiveProgress(
    page,
    atom_key="upload_progress",
    title="Upload Progress",
    max_value=100,
    color=ft.Colors.BLUE_700
)

page.add(progress.control)

# Update progress
progress.set(50)       # Set to 50%
progress.increment(5)  # Add 5%
progress.complete()    # Jump to 100%
progress.reset()       # Back to 0%
```

**Features:**
- ✅ Automatic percentage display
- ✅ Progress bar visualization
- ✅ Configurable max value
- ✅ Helper methods (increment, complete, reset)

## 🚀 Running the Example

```bash
# From project root
python examples/16_reactive_atomic_components/main.py

# Or as a module
python -m examples.16_reactive_atomic_components.main
```

## 💎 Key Benefits

### 1. **Encapsulation**
```python
# Everything in one place
counter = ReactiveCounter(page, "Counter", 0)
# State atom ✅ UI component ✅ Binding ✅
```

### 2. **Reusability**
```python
# Create multiple instances easily
counter1 = ReactiveCounter(page, "A", 0)
counter2 = ReactiveCounter(page, "B", 10)
counter3 = ReactiveCounter(page, "C", 100)
```

### 3. **Clean API**
```python
# Intuitive methods
counter.increment()
counter.decrement()
counter.reset()
print(counter.value)
```

### 4. **Automatic Updates**
```python
# Change state → UI updates automatically
counter.set(42)  # ✨ Display updates instantly
```

### 5. **Type Safety**
```python
# Each component knows its type
users_card: ReactiveStatCard
username: ReactiveInput
progress: ReactiveProgress
```

## 🎨 Real-World Use Cases

### Dashboard with Live Updates

```python
# Create dashboard metrics
users = ReactiveStatCard(page, "Users", "users", "1,234", ft.Icons.PEOPLE)
revenue = ReactiveStatCard(page, "Revenue", "revenue", "$45K", ft.Icons.ATTACH_MONEY)

# Auto-update in background
def update_metrics():
    while True:
        time.sleep(5)
        users.set(f"{random.randint(1000, 2000):,}")
        revenue.set(f"${random.randint(40, 60)}K")

threading.Thread(target=update_metrics, daemon=True).start()
```

### Multi-Step Form Wizard

```python
# Step 1: Personal info
step1 = ReactiveForm(page, "step1", "Personal Info", [
    {"key": "name", "label": "Name"},
    {"key": "age", "label": "Age"}
])

# Step 2: Contact info
step2 = ReactiveForm(page, "step2", "Contact Info", [
    {"key": "email", "label": "Email"},
    {"key": "phone", "label": "Phone"}
])

# Navigate between steps
def next_step(e):
    step1_data = step1.get()
    # Validate and move to step2...
```

### File Upload with Progress

```python
upload_progress = ReactiveProgress(page, "upload", "Uploading...", 100)

async def upload_file(file_path):
    # Simulate upload
    for i in range(0, 101, 10):
        await asyncio.sleep(0.1)
        upload_progress.set(i)

    # Complete
    upload_progress.complete()
```

## 🔄 Component Lifecycle

```python
# 1. Create component (atom + UI + binding)
counter = ReactiveCounter(page, "Counter", 0)

# 2. Add to page
page.add(counter.control)

# 3. Interact via API
counter.increment()  # State changes
# ↓
# Atom updates
# ↓
# UI updates automatically ✨

# 4. Listen to changes
counter.listen(lambda value: print(f"New value: {value}"))

# 5. Clean up (automatic via garbage collection)
```

## 🎓 Advanced Patterns

### Computed Values from Multiple Components

```python
counter_a = ReactiveCounter(page, "A", 0)
counter_b = ReactiveCounter(page, "B", 0)
sum_display = ReactiveText(page, "sum", "0")

def update_sum():
    total = counter_a.value + counter_b.value
    sum_display.set(str(total))

counter_a.listen(lambda _: update_sum())
counter_b.listen(lambda _: update_sum())
```

### Conditional Rendering Based on State

```python
count_display = ReactiveCounter(page, "Count", 0)

def check_value(value):
    if value > 10:
        # Show warning
        page.snack_bar = ft.SnackBar(ft.Text("Value exceeds 10!"))
        page.snack_bar.open = True
        page.update()

count_display.listen(check_value, immediate=False)
```

### Form Validation

```python
form = ReactiveForm(page, "login", "Login", [
    {"key": "email", "label": "Email"},
    {"key": "password", "label": "Password", "password": True}
])

def validate_and_submit(data):
    if "@" not in data["email"]:
        page.snack_bar = ft.SnackBar(ft.Text("Invalid email!"))
        page.snack_bar.open = True
        page.update()
        return

    # Proceed with login...
    print("Login successful!")

form.on_submit = validate_and_submit
```

## 🐛 Troubleshooting

**Q: My component doesn't update**
```python
# Make sure you're calling set(), not modifying the atom directly
counter.set(42)  # ✅ Correct
page.state.set(counter.atom_key, 42)  # ❌ Don't do this
```

**Q: How do I access the underlying atom?**
```python
# Use the atom_key property
atom_key = counter.atom_key
raw_value = page.state.get(atom_key)
```

**Q: Can I customize the UI?**
```python
# Yes! Access the control property and modify
counter.control.bgcolor = ft.Colors.RED_50
counter.control.border = ft.border.all(3, ft.Colors.RED_700)
page.update()
```

## 📚 Learn More

- [Atomic Design Methodology](https://atomicdesign.bradfrost.com/)
- [Flet-ASP Documentation](https://github.com/brunobrown/flet-asp)
- [Example 14: Atomic Design Dashboard](../14_atomic_design_dashboard/)
- [Example 15: Theming System](../15_atomic_design_theming/)

## 🎯 Next Steps

1. **Create your own reactive components** - Extend `ReactiveAtom`
2. **Build a complete app** - Use reactive components throughout
3. **Share your components** - Package them for reuse
4. **Combine with Example 15** - Add theming support