# Example 15: Atomic Design with Dynamic Theming

An advanced component library demonstrating **theme-aware design systems** built with Atomic Design principles and flet-asp reactive state management.

## 🎯 What You'll Learn

- Building theme-aware design systems with design tokens
- Creating reusable components that adapt to light/dark modes
- Real-time theme switching with flet-asp state management
- Professional design system architecture
- Scaling design tokens across component hierarchies

## 📁 Project Structure

```
15_atomic_design_theming/
├── __init__.py          # Package initialization
├── theme_tokens.py      # Design tokens (colors, typography, spacing)
├── atoms.py             # Theme-aware basic elements
├── molecules.py         # Theme-aware component combinations
├── main.py              # Component library showcase
└── README.md            # This file
```

## 🎨 Design Token System

### What are Design Tokens?

Design tokens are the most atomic level of a design system - they're named values that define your visual language:

- **Colors**: Primary, secondary, semantic colors
- **Typography**: Font sizes, weights, line heights
- **Spacing**: Consistent spacing scale (xs, sm, md, lg, xl)
- **Radii**: Border radius values

### Theme Tokens Structure

```python
from theme_tokens import get_theme

theme = get_theme()

# Access color tokens
theme.colors.primary           # Primary brand color
theme.colors.background        # Page background
theme.colors.text_primary      # Primary text color

# Access typography tokens
theme.typography.headline_large  # 32px
theme.typography.body_medium     # 14px

# Access spacing tokens
theme.spacing.xs    # 4px
theme.spacing.md    # 16px
theme.spacing.xl    # 32px

# Access radius tokens
theme.radius.sm     # 4px
theme.radius.lg     # 12px
```

### Light vs Dark Themes

The theme system automatically provides appropriate tokens for each mode:

| Token | Light Mode | Dark Mode |
|-------|-----------|-----------|
| `colors.primary` | Blue 700 | Blue 400 |
| `colors.background` | Grey 50 | Grey 900 |
| `colors.surface` | White | Grey 800 |
| `colors.text_primary` | Grey 900 | Grey 100 |

## 🔬 Theme-Aware Components

### Theme-Aware Atoms

All atoms use theme tokens instead of hardcoded colors:

```python
from atoms import headline_text, filled_button, text_field

# These automatically adapt to the current theme!
title = headline_text("Welcome", level=1)
button = filled_button("Submit", on_click=handler)
input_field = text_field(label="Name")
```

**Available atoms:**
- Text: `display_text`, `headline_text`, `title_text`, `body_text`, `label_text`
- Buttons: `filled_button`, `outlined_button`, `text_button`, `icon_button`
- Inputs: `text_field`, `dropdown_field`, `checkbox`, `switch`
- Icons: `icon` (with semantic coloring)
- Dividers: `divider`, `vertical_divider`
- Containers: `card`, `surface`, `chip`

### Theme-Aware Molecules

Molecules combine atoms while preserving theme awareness:

```python
from molecules import stat_card, alert, input_group

# Stat card with semantic coloring
card = stat_card(
    label="Revenue",
    value="$89,432",
    icon_name=ft.Icons.ATTACH_MONEY,
    trend="+8.3%",
    trend_positive=True,
)

# Alert with severity-based colors
alert_widget = alert(
    message="Success!",
    severity="success",  # Automatically colored
    dismissible=True,
)

# Input group with validation
field = input_group(
    label="Email",
    help_text="We'll never share your email",
    error=None,  # or "Invalid email"
)
```

**Available molecules:**
- `alert` - Colored notification banners
- `input_group` - Label + input + help/error text
- `stat_card` - Metric display with trend indicator
- `list_item` - Title + subtitle with icons
- `avatar` - User avatar with initials
- `badge` - Colored label tags
- `theme_toggle` - Light/dark mode switcher

## 🔄 Reactive Theme Switching

### How It Works

1. **Theme tokens** define colors for light/dark modes
2. **Components** use tokens instead of hardcoded values
3. **State management** tracks current theme mode
4. **Theme changes** trigger UI rebuild with new tokens

### Implementation

```python
import flet_asp as fa
from theme_tokens import get_theme

# 1. Initialize state
fa.get_state_manager(page)
theme = get_theme()

# 2. Create theme mode atom
page.state.atom("theme_mode", "light")

# 3. Theme toggle handler
def toggle_theme():
    current = page.state.get("theme_mode")
    new_mode = "dark" if current == "light" else "light"
    page.state.set("theme_mode", new_mode)

    # Update theme and rebuild UI
    theme.mode = new_mode
    rebuild_ui()

# 4. Rebuild UI with current theme
def rebuild_ui():
    theme = get_theme()
    page.bgcolor = theme.colors.background
    # ... build components using theme tokens
```

## 🚀 Running the Example

```bash
# From project root
python examples/15_atomic_design_theming/main.py

# Or as a module
python -m examples.15_atomic_design_theming.main
```

## ✨ Features

### 1. **Live Theme Switching**
Toggle between light and dark modes with the theme switch. All components update instantly!

### 2. **Semantic Colors**
Components like alerts and badges use semantic colors (success, warning, error, info) that adapt to the theme.

### 3. **Consistent Spacing**
All spacing uses the token system for perfect consistency across components.

### 4. **Accessible Contrast**
Dark mode automatically provides high-contrast colors for accessibility.

### 5. **Component Showcase**
See all components in action: stats, alerts, buttons, forms, lists, badges.

## 🎨 Customizing the Theme

### Adding New Colors

```python
# theme_tokens.py
LIGHT_COLORS = ColorTokens(
    # ... existing colors
    accent=ft.Colors.PURPLE_700,  # Add custom color
)

DARK_COLORS = ColorTokens(
    # ... existing colors
    accent=ft.Colors.PURPLE_400,  # Dark mode version
)
```

### Using Custom Colors

```python
# atoms.py
def accent_button(text: str, on_click=None):
    theme = get_theme()
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        bgcolor=theme.colors.accent,  # Use custom color
    )
```

### Adjusting Typography

```python
# theme_tokens.py
TYPOGRAPHY = TypographyTokens(
    headline_large=36,  # Increase from 32
    body_medium=16,     # Increase from 14
)
```

## 📚 Design System Best Practices

### 1. **Always Use Tokens**
❌ Don't: `color=ft.Colors.BLUE_700`
✅ Do: `color=theme.colors.primary`

### 2. **Semantic Naming**
Use meaningful names like `primary`, `surface`, `text_primary` instead of color names.

### 3. **Consistent Spacing**
Use the spacing scale for all margins and padding:
```python
padding=theme.spacing.md  # Not padding=16
```

### 4. **Build Up from Atoms**
Create complex UIs by composing simple, theme-aware components.

### 5. **Test Both Themes**
Always test components in both light and dark modes.

## 🔧 Advanced Techniques

### Theme-Aware Shadows

```python
def elevated_card(content):
    theme = get_theme()
    shadow_color = (
        ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
        if theme.mode == "light"
        else ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
    )

    return ft.Container(
        content=content,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=shadow_color,
        ),
    )
```

### Conditional Theme Logic

```python
def adaptive_component():
    theme = get_theme()

    if theme.mode == "dark":
        # Dark mode specific behavior
        pass
    else:
        # Light mode specific behavior
        pass
```

### Theme Observers

```python
# Register callback for theme changes
def on_theme_change(new_mode):
    print(f"Theme changed to: {new_mode}")

theme.observe(on_theme_change)
```

## 💡 Use Cases

### 1. **Multi-Tenant Applications**
Each tenant can have custom brand colors while maintaining consistent structure.

### 2. **Accessibility Features**
Provide high-contrast themes for users with visual impairments.

### 3. **User Preferences**
Let users choose their preferred theme and persist it.

### 4. **Brand Guidelines**
Enforce consistent design across teams using shared tokens.

## 🐛 Troubleshooting

**Issue: Components not updating after theme change**
- Ensure you're rebuilding the UI after setting `theme.mode`
- Check that components are using `theme.colors` not hardcoded colors

**Issue: Colors look wrong in dark mode**
- Verify both LIGHT_COLORS and DARK_COLORS are properly defined
- Test contrast ratios for accessibility

**Issue: Spacing inconsistent**
- Always use `theme.spacing.*` instead of hardcoded values
- Check that all containers use the spacing scale

## 📚 Learn More

- [Atomic Design Methodology](https://atomicdesign.bradfrost.com/)
- [Design Tokens Community Group](https://www.designtokens.org/)
- [Material Design - Theming](https://m3.material.io/foundations/customization)
- [Flet-ASP Documentation](https://github.com/brunobrown/flet-asp)

## 🎓 Next Steps

1. **Add more themes**: Create additional color schemes (e.g., high contrast, colorblind-friendly)
2. **Persistent preferences**: Save theme choice to local storage
3. **Theme builder**: Create UI for users to customize their theme