# panel-siemens-ix

A Siemens Industrial Experience (iX) compliant theme library for [`panel-material-ui`](https://panel-material-ui.readthedocs.io/).

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

## Usage Examples

To apply the Siemens iX theme to your `panel-material-ui` application, you can use the `create_siemens_ix_theme` function or the convenience aliases `siemens_ix_light_theme` and `siemens_ix_dark_theme`.

### Applying a Light Theme

```python
import panel as pn
from panel_material_ui import MaterialTemplate
from panel_material_ui.theme import MaterialLightTheme
from panel_siemens_ix.theme import siemens_ix_light_theme

pn.extension('material-ui', template='material', sizing_mode='stretch_width')

# Create a Material-UI template with the Siemens iX light theme
template = MaterialTemplate(
    site="Siemens iX App",
    title="Light Theme Example",
    theme=MaterialLightTheme(siemens_ix_light_theme()),
)

# Example content
template.main.append(pn.widgets.Button(name="Primary Button", button_type="primary"))
template.main.append(pn.widgets.Button(name="Secondary Button", button_type="default"))
template.main.append(pn.widgets.TextInput(name="Text Input", value="Hello Siemens iX!"))

template.servable()
```

### Applying a Dark Theme

```python
import panel as pn
from panel_material_ui import MaterialTemplate
from panel_material_ui.theme import MaterialDarkTheme
from panel_siemens_ix.theme import siemens_ix_dark_theme

pn.extension('material-ui', template='material', sizing_mode='stretch_width')

# Create a Material-UI template with the Siemens iX dark theme
template = MaterialTemplate(
    site="Siemens iX App",
    title="Dark Theme Example",
    theme=MaterialDarkTheme(siemens_ix_dark_theme()),
)

# Example content
template.main.append(pn.widgets.Button(name="Primary Button", button_type="primary"))
template.main.append(pn.widgets.Button(name="Secondary Button", button_type="default"))
template.main.append(pn.widgets.TextInput(name="Text Input", value="Hello Siemens iX!"))

template.servable()
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