# Panel Siemens iX Examples

This directory contains comprehensive examples demonstrating how to use the `panel-siemens-ix` library to create applications that follow the Siemens iX design system. All examples follow Panel best practices including parameter-driven architecture, proper reactive patterns, and modern serving approaches.

## Quick Start

The fastest way to get started is with the basic examples:

```bash
# Install dependencies
uv sync --group dev

# Run a basic example
cd examples/basic
panel serve minimal_app.py --dev --show
```

## Directory Structure

### 📁 [basic/](basic/) - Getting Started
Start here if you're new to panel-siemens-ix or Panel Material UI:

- **[minimal_app.py](basic/minimal_app.py)** - Simplest possible working example
- **[quick_start.py](basic/quick_start.py)** - Using the `configure()` function for instant setup
- **[theme_switching.py](basic/theme_switching.py)** - Light/dark theme toggle with ThemeToggle
- **[component_showcase.py](basic/component_showcase.py)** - Common Material UI components with Siemens iX styling

### 📁 [applications/](applications/) - Real-World Examples
Complete applications demonstrating Panel best practices:

- **[dashboard.py](applications/dashboard.py)** - Interactive dashboard with parameter-driven design
- **[data_form.py](applications/data_form.py)** - Form with validation using Panel patterns
- **[analytics_viewer.py](applications/analytics_viewer.py)** - Data visualization with plots and interactivity
- **[settings_panel.py](applications/settings_panel.py)** - Configuration interface with reactive state management

### 📁 [components/](components/) - Component Gallery
Deep dive into specific Material UI components:

- **[buttons.py](components/buttons.py)** - All button variants, interactions, and event handling
- **[inputs_and_selectors.py](components/inputs_and_selectors.py)** - Text inputs, selectors, sliders with validation
- **[layouts.py](components/layouts.py)** - Material UI layouts (Grid, FlexBox, Container, etc.)
- **[feedback.py](components/feedback.py)** - Alerts, progress indicators, notifications
- **[navigation.py](components/navigation.py)** - Tabs, Accordion, Breadcrumbs, and navigation patterns

### 📁 [advanced/](advanced/) - Advanced Techniques
For experienced developers wanting to push the boundaries:

- **[custom_theming.py](advanced/custom_theming.py)** - Advanced theme customization techniques
- **[reactive_components.py](advanced/reactive_components.py)** - Complex parameter-driven reactive design
- **[integration_demo.py](advanced/integration_demo.py)** - Integration with external plots and visualizations
- **[performance_tips.py](advanced/performance_tips.py)** - Optimized patterns, caching, and performance
- **[time_series_dashboard.py](advanced/time_series_dashboard.py)** - Comprehensive data analytics dashboard with interactive time series visualizations
- **[bi_dashboard.py](advanced/bi_dashboard.py)** - Business intelligence dashboard with data catalog, SQL editor, and visualization

### 📁 [utilities/](utilities/) - Helper Functions and Tools
Working with colors, assets, and theme utilities:

- **[color_palette_demo.py](utilities/color_palette_demo.py)** - Color utilities and palette generation
- **[brand_assets.py](utilities/brand_assets.py)** - Logo and brand asset usage patterns
- **[theme_creation.py](utilities/theme_creation.py)** - Creating custom themes from scratch

## Panel Best Practices Used

All examples in this directory follow Panel's recommended patterns:

### Parameter-Driven Architecture
- ✅ Use `param.Parameterized` or `pn.viewable.Viewer` classes
- ✅ Create widgets with `.from_param()` method
- ✅ Use `@param.depends()` for reactive methods
- ✅ Avoid `.watch()` for UI updates (only for side effects)

### Layout and UI Best Practices
- ✅ Use `sizing_mode="stretch_width"` by default
- ✅ Create static layout with reactive content
- ✅ Use Material UI `Page` component for templates
- ✅ Proper sidebar organization: logo → description → inputs → docs

### Serving Patterns
- ✅ Include both development and production serving patterns
- ✅ Use `panel serve app.py --dev` for development
- ✅ Proper `.servable()` component marking
- ✅ `if __name__ == "__main__":` and `if pn.state.served:` patterns

### Component Selection
- ✅ Material UI components with Siemens iX theming
- ✅ `pn.widgets.Tabulator` for tabular data
- ✅ Proper extension loading with `pn.extension()`
- ✅ Accessibility and responsive design considerations

## Running Examples

### Individual Examples
```bash
# Navigate to any example directory
cd examples/basic

# Run with development server (hot reload)
panel serve minimal_app.py --dev --show

# Or run directly with Python
python minimal_app.py
```

### All Examples at Once
```bash
# From the root directory
panel serve examples/**/*.py --dev --show
```

## Panel Material UI Integration

These examples demonstrate how `panel-siemens-ix` seamlessly integrates with `panel-material-ui`:

```python
import panel as pn
import panel_material_ui as pmui
from panel_siemens_ix import configure

# Enable Material UI extension
pn.extension()

# Apply complete Siemens iX branding
configure()

# Create a Page with Siemens iX theme
page = pmui.Page(
    title="My Siemens iX App",
    main=[
        pmui.Button(name="Primary Button", button_type="primary"),
        pmui.TextField(name="Input", placeholder="Enter text..."),
    ]
)

page.servable()
```

## Design System Features

The examples showcase these Siemens iX design system features:

- **🎨 Color System**: Full light/dark theme support with semantic colors
- **📝 Typography**: Siemens Sans font family with proper hierarchy
- **🖱️ Components**: Material UI components styled to match Siemens iX
- **📱 Responsive**: Mobile-first responsive design patterns
- **♿ Accessibility**: WCAG compliant color contrasts and interactions
- **🏢 Branding**: Siemens logos, favicons, and brand assets

## Contributing

When adding new examples:

1. Follow Panel's parameter-driven architecture
2. Include both development and production serving patterns
3. Add comprehensive docstrings and comments
4. Test with both light and dark themes
5. Ensure responsive design works on mobile
6. Include error handling and validation where appropriate

## Resources

- [Panel Documentation](https://panel.holoviz.org/)
- [Panel Material UI Documentation](https://panel-material-ui.holoviz.org/)
- [Siemens iX Design System](https://ix.siemens.io/)
- [Material-UI Documentation](https://mui.com/material-ui/)

---

*💡 **Tip**: Start with the [basic examples](basic/) and gradually progress to more advanced patterns. Each example is self-contained and can be run independently.*