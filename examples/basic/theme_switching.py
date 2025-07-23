"""
Theme Switching with Siemens iX

This example demonstrates how to implement light/dark theme switching using 
the Material UI ThemeToggle component with Siemens iX themes. It showcases
how colors, components, and layouts adapt seamlessly between themes.

Run with:
    panel serve theme_switching.py --dev --show
Or:
    python theme_switching.py
"""

import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme
from panel_siemens_ix.colors import get_colors


class ThemeSwitchingDemo(pn.viewable.Viewer):
    """
    Demonstration of theme switching with Siemens iX color system.
    
    This example shows how different components and colors adapt
    automatically when switching between light and dark themes.
    """
    
    sample_text = param.String(
        default="Welcome to Siemens iX theming!",
        doc="Sample text to demonstrate typography"
    )
    progress_value = param.Number(
        default=75, bounds=(0, 100),
        doc="Progress bar value for demonstration"
    )
    alert_visible = param.Boolean(
        default=True,
        doc="Whether to show the alert component"
    )
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_components()
            self._create_layout()
    
    def _create_components(self):
        """Create components that demonstrate theme switching."""
        
        # Color demonstration section
        self._color_demo = self._create_color_demo()
        
        # Typography demonstration
        self._typography_demo = self._create_typography_demo()
        
        # Component demonstration
        self._component_demo = self._create_component_demo()
        
        # Interactive controls
        self._controls_demo = self._create_controls_demo()
    
    def _create_color_demo(self):
        """Create color palette demonstration."""
        
        def create_color_chip(color_name, description):
            """Helper to create color demonstration chips."""
            return pmui.Chip(
                label=f"{color_name}: {description}",
                color=color_name.lower() if color_name.lower() in ['primary', 'secondary', 'error', 'warning', 'info', 'success'] else 'primary',
                styles={"margin": "4px"}
            )
        
        color_chips = [
            create_color_chip("Primary", "Main brand color"),
            create_color_chip("Secondary", "Supporting color"),
            create_color_chip("Success", "Positive actions"),
            create_color_chip("Warning", "Caution states"),
            create_color_chip("Error", "Error states"),
            create_color_chip("Info", "Information states"),
        ]
        
        return pmui.Card(
            pmui.Typography("Color System", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "These chips demonstrate how Siemens iX semantic colors adapt between themes:",
                variant="body2",
                styles={"marginBottom": "15px"}
            ),
            pmui.Row(*color_chips, styles={"flexWrap": "wrap"}),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_typography_demo(self):
        """Create typography demonstration."""
        return pmui.Card(
            pmui.Typography("Typography System", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography("Heading 1 - Siemens Sans", variant="h1"),
            pmui.Typography("Heading 2 - Siemens Sans", variant="h2"),
            pmui.Typography("Heading 3 - Siemens Sans", variant="h3"),
            pmui.Typography("Body text demonstrates how text colors adapt automatically between light and dark themes. The Siemens Sans font family provides excellent readability.", variant="body1"),
            pmui.Typography("Caption text in Siemens Sans", variant="caption"),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_component_demo(self):
        """Create component demonstration."""
        
        # Progress indicator
        progress_display = pmui.Column(
            pmui.Typography(f"Progress: {self.progress_value}%", variant="body1"),
            pmui.LinearProgress(
                value=self.progress_value,
                color="primary",
                styles={"margin": "10px 0"}
            ),
            pmui.CircularProgress(
                value=self.progress_value,
                color="secondary",
                size=30,
                styles={"alignSelf": "center", "margin": "10px"}
            )
        )
        
        # Alert component
        alert_component = pmui.Alert(
            object="🎨 Notice how this alert adapts its colors based on the current theme!",
            alert_type="info",
            visible=self.alert_visible,
            styles={"margin": "10px 0"}
        )
        
        return pmui.Card(
            pmui.Typography("Component Adaptation", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "Watch how these components automatically adapt their styling:",
                variant="body2",
                styles={"marginBottom": "15px"}
            ),
            progress_display,
            alert_component,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_controls_demo(self):
        """Create interactive controls demonstration."""
        
        # Sample buttons with different styles
        button_row = pmui.Row(
            pmui.Button(
                name="Primary Button",
                button_type="primary",
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Secondary Button", 
                button_type="secondary",
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Outlined",
                button_type="primary",
                variant="outlined",
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Text Button",
                button_type="primary",
                variant="text",
                styles={"margin": "5px"}
            ),
            styles={"flexWrap": "wrap"}
        )
        
        # Input components
        sample_input = pmui.TextInput.from_param(
            self.param.sample_text,
            name="Sample Text",
            placeholder="Type something...",
            styles={"margin": "10px 0"}
        )
        
        progress_slider = pmui.IntSlider.from_param(
            self.param.progress_value,
            name="Progress Value",
            styles={"margin": "10px 0"}
        )
        
        alert_toggle = pmui.Switch.from_param(
            self.param.alert_visible,
            name="Show Alert"
        )
        
        return pmui.Card(
            pmui.Typography("Interactive Components", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "These controls demonstrate interactive components with theme-aware styling:",
                variant="body2",
                styles={"marginBottom": "15px"}
            ),
            button_row,
            sample_input,
            progress_slider,
            alert_toggle,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_layout(self):
        """Create the main application layout."""
        
        # Header with theme switching instructions
        header = pmui.Paper(
            pmui.Typography(
                "🌓 Theme Switching Demo", 
                variant="h4",
                styles={"textAlign": "center", "marginBottom": "10px"}
            ),
            pmui.Typography(
                "Use the theme toggle in the top-right corner to switch between light and dark modes.",
                variant="body1",
                styles={"textAlign": "center", "marginBottom": "10px"}
            ),
            pmui.Alert(
                object="💡 Pro tip: Notice how all colors, shadows, and component styles adapt automatically!",
                alert_type="success"
            ),
            styles={"padding": "30px", "marginBottom": "20px"}
        )
        
        # Main content in a container for proper responsive behavior
        self._layout = pmui.Container(
            header,
            self._color_demo,
            self._typography_demo, 
            self._component_demo,
            self._controls_demo,
            width_option="lg"  # Large responsive breakpoint
        )
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """
        Create a servable app with theme switching capabilities.
        
        This demonstrates how to set up both light and dark themes
        and enable the theme toggle functionality.
        """
        instance = cls(**params)
        
        # Create Page with both theme configurations
        page = pmui.Page(
            title="Theme Switching - Siemens iX",
            # DO provide theme configuration for both modes
            theme_config={
                "light": siemens_ix_light_theme,
                "dark": siemens_ix_dark_theme
            },
            main=[instance],
            sidebar=[
                pmui.Typography("Theme Information", variant="h6"),
                pmui.Typography(
                    "Current theme colors adapt automatically:",
                    variant="body2",
                    styles={"marginBottom": "15px"}
                ),
                pmui.Paper(
                    pmui.Typography("Light Theme", variant="subtitle2"),
                    pmui.Typography("• Clean, bright appearance", variant="body2"),
                    pmui.Typography("• High contrast for readability", variant="body2"),
                    pmui.Typography("• Professional look", variant="body2"),
                    styles={"padding": "15px", "margin": "10px 0"}
                ),
                pmui.Paper(
                    pmui.Typography("Dark Theme", variant="subtitle2"),
                    pmui.Typography("• Reduced eye strain", variant="body2"),
                    pmui.Typography("• Modern appearance", variant="body2"),
                    pmui.Typography("• Better for low-light environments", variant="body2"),
                    styles={"padding": "15px", "margin": "10px 0"}
                ),
            ],
            # DO enable theme toggle for user control
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python theme_switching.py`
    ThemeSwitchingDemo.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve theme_switching.py --port 5007 --dev --show`
    ThemeSwitchingDemo.create_app().servable()