# panel-siemens-ix

A Siemens Industrial Experience (iX) compliant theme library for [`panel-material-ui`](https://panel-material-ui.holoviz.org/).

## Screenshots

Below are visual examples of the Siemens iX theme in both light and dark modes:

| Light Theme | Dark Theme |
|:-----------:|:----------:|
| ![Light Theme](docs/screenshots/light.png) | ![Dark Theme](docs/screenshots/dark.png) |

## Purpose

`panel-siemens-ix` provides a comprehensive theme solution for applications built with `panel-material-ui`, ensuring they adhere to the strict design guidelines of Siemens iX Open Source Design. This library offers a seamless way to integrate the distinct visual language of Siemens iX into your Panel applications, making it easier to develop consistent and high-quality user interfaces.

## Key Features

*   **Full Siemens iX Open Source Design Compliance:** Adheres to the official Siemens iX design guidelines, including:
    *   **Color Palette:** Accurate implementation of iX color specifications for both light and dark themes, including hover and active states.
    *   **Typography:** Correct font families, sizes, and weights for headings and body text.
    *   **Spacing:** Consistent use of spacing units to ensure visual harmony.
    *   **Component Styling:** Theming of common Material-UI components (e.g., Buttons, Chips, TextFields, Paper, AppBar) to match iX aesthetics.
*   **Light and Dark Themes:** Supports both light and dark modes, allowing users to switch between preferred visual styles.
*   **Seamless Integration:** Designed to work effortlessly with `panel-material-ui`, extending its capabilities with iX-specific styling.

## Installation

You can install `panel-siemens-ix` using `pip`:

```bash
pip install panel-siemens-ix
```

Or with `uv`:

```bash
uv pip install panel-siemens-ix
```

## Quick Start

The easiest way to get started is using the `configure()` function for complete setup:

```python
import panel as pn
import panel_material_ui as pmui
from panel_siemens_ix import configure

# Apply complete Siemens iX configuration
configure()

# Enable Panel extensions
pn.extension()

# Create your app with Material UI components
app = pmui.Page(
    title="My Siemens iX App",
    main=[
        pmui.Button(name="Primary Action", button_type="primary"),
        pmui.TextInput(name="Input Field", placeholder="Enter text..."),
        pmui.Alert(object="Welcome to Siemens iX!", alert_type="success")
    ],
    theme_toggle=True  # Enable light/dark theme switching
)

app.servable()
```

## Usage Examples

### 1. Basic Application

```python
import panel as pn
import panel_material_ui as pmui
from panel_siemens_ix import configure

# Apply Siemens iX configuration
configure()
pn.extension()

# Simple app with Material UI components
def create_basic_app():
    return pmui.Container(
        pmui.Typography("Welcome to Siemens iX", variant="h4"),
        pmui.Button(
            name="Get Started", 
            button_type="primary",
            icon="rocket_launch"
        ),
        pmui.TextInput(
            name="Your Name",
            placeholder="Enter your name..."
        )
    )

# Serve the app
create_basic_app().servable()
```

### 2. Parameter-Driven Application (Recommended)

```python
import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix import configure

configure()
pn.extension()

class MyApp(pn.viewable.Viewer):
    """Parameter-driven app following Panel best practices."""
    
    # App parameters
    text_input = param.String(default="Hello Siemens iX!")
    number_value = param.Number(default=42, bounds=(0, 100))
    
    def __init__(self, **params):
        super().__init__(**params)
        self._create_layout()
    
    def _create_layout(self):
        """Create the app layout."""
        self._layout = pmui.Container(
            pmui.Typography("Parameter-Driven App", variant="h4"),
            pmui.TextInput.from_param(
                self.param.text_input,
                name="Text Input"
            ),
            pmui.FloatInput.from_param(
                self.param.number_value,
                name="Number Input"
            ),
            pmui.Typography(
                object=self.status_display,
                variant="body1"
            )
        )
    
    @param.depends("text_input", "number_value")
    def status_display(self):
        """Reactive status display."""
        return f"Current values: '{self.text_input}' and {self.number_value}"
    
    def __panel__(self):
        """Return the layout for Panel."""
        return self._layout

# Create and serve the app
MyApp().servable()
```

### 3. Using Custom Themes

For advanced customization, you can use the theme functions directly:

```python
import panel as pn
import panel_material_ui as pmui
from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme

pn.extension()

# Create a page with both light and dark themes
app = pmui.Page(
    title="Custom Theme App",
    main=[
        pmui.Typography("Custom Siemens iX Theme", variant="h4"),
        pmui.Button(name="Primary Button", button_type="primary"),
        pmui.Alert(object="Themed with Siemens iX colors!", alert_type="info")
    ],
    # Configure both themes
    theme_config={
        "light": siemens_ix_light_theme,
        "dark": siemens_ix_dark_theme
    },
    theme_toggle=True
)

app.servable()
```

## Example Applications

The `examples/` directory contains comprehensive example applications:

### Basic Examples
- **`minimal_app.py`** - Simplest possible Siemens iX app
- **`quick_start.py`** - Quick start template with common components
- **`showcase_compact.py`** - Compact showcase of key components (fits without scrolling)
- **`component_showcase.py`** - Comprehensive showcase of Material UI components
- **`theme_switching.py`** - Light/dark theme switching demonstration

### Application Examples
- **`applications/dashboard.py`** - Industrial dashboard with KPIs and charts
- **`applications/data_form.py`** - Data entry form with validation

### Utility Examples
- **`utilities/color_palette_demo.py`** - Interactive color system explorer

### Running Examples

```bash
# Run any example directly
python examples/basic/showcase_compact.py

# Or serve with Panel
panel serve examples/basic/showcase_compact.py --dev --show

# Other examples
python examples/basic/component_showcase.py

# View all examples
ls examples/
```

Each example demonstrates Panel best practices including:
- Parameter-driven architecture
- Reactive programming with `@param.depends`
- Proper Material UI component usage
- Siemens iX theming integration

## Color System

The library includes a comprehensive color system with semantic colors for both light and dark themes:

```python
from panel_siemens_ix.colors import get_colors, get_continuous_cmap, get_categorical_palette

# Get colors for current theme
colors = get_colors("light")  # or "dark"

# Access semantic colors
primary_color = colors.primary["main"]
success_color = colors.success["main"]
warning_color = colors.warning["main"]

# Generate palettes for data visualization
categorical_palette = get_categorical_palette(dark_theme=False, n_colors=8)
continuous_colormap = get_continuous_cmap(dark_theme=False)
```

### Available Color Categories
- **Semantic Colors**: primary, secondary, success, warning, error, info
- **Component Colors**: text, background, border, ghost
- **Interactive States**: main, hover, active, disabled

## Configuration Options

### Full Configuration
```python
from panel_siemens_ix import configure

# Apply complete Siemens iX setup
configure()
```

This sets up:
- Siemens logos and branding
- Custom favicon
- Theme configuration
- Default component styles
- Panel-specific optimizations

### Manual Theme Configuration
```python
import panel_material_ui as pmui
from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme

# Apply themes manually to a Page
app = pmui.Page(
    theme_config={
        "light": siemens_ix_light_theme,
        "dark": siemens_ix_dark_theme
    },
    theme_toggle=True
)
```

## Development

### Project Structure
```
panel-siemens-ix/
├── src/panel_siemens_ix/
│   ├── __init__.py          # Main configuration
│   ├── theme.py             # Theme creation functions
│   ├── colors.py            # Color system
│   └── static/              # Brand assets (logos, favicons)
├── examples/                # Example applications
│   ├── basic/              # Basic usage examples
│   ├── applications/       # Complete applications
│   └── utilities/          # Utility demonstrations
└── colors/                 # Color extraction tools
```



## Design Principles

`panel-siemens-ix` is built upon the core principles of the Siemens iX Open Source Design system, ensuring:

*   **Consistency:** Provides a unified look and feel across your applications, reducing visual clutter and improving user recognition.
*   **Clarity:** Emphasizes clear visual hierarchies and legible elements to enhance user comprehension and interaction.
*   **Usability:** Focuses on intuitive and accessible design patterns to create a positive user experience.

By leveraging this library, developers can quickly and confidently create Panel applications that align with Siemens' brand identity and user experience standards.

## Contribution Guidelines

Contributions are welcome! If you'd like to contribute to `panel-siemens-ix`, please refer to the project's [CONTRIBUTING.md](CONTRIBUTING.md) file (if available) or open an issue/pull request on the GitHub repository.

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file (if available) for details.