"""
Quick Start with panel-siemens-ix

This example demonstrates the easiest way to get started with panel-siemens-ix
using the configure() function. This function automatically applies all Siemens iX
branding including themes, logos, favicons, and component defaults.

Run with:
    panel serve quick_start.py --dev --show
Or:
    python quick_start.py
"""

import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix import configure


class QuickStartApp(pn.viewable.Viewer):
    """
    Quick start application showcasing the power of configure().
    
    The configure() function provides:
    - Automatic theme configuration for both light and dark modes
    - Siemens logos and favicon
    - Material UI component defaults
    - Proper branding colors and styles
    """
    
    counter = param.Integer(default=0, bounds=(0, None), doc="Click counter")
    user_input = param.String(default="", doc="User text input")
    selected_option = param.Selector(
        default="Option 1", 
        objects=["Option 1", "Option 2", "Option 3"],
        doc="Selected option from dropdown"
    )
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_widgets()
            self._create_layout()
    
    def _create_widgets(self):
        """Create Material UI widgets with Siemens iX theming."""
        
        # DO create widgets using .from_param method for reactive behavior
        self._counter_display = pmui.Typography(
            object=self.counter_display,
            variant="h5",
            styles={"textAlign": "center", "margin": "20px 0"}
        )
        
        self._increment_button = pmui.Button(
            name="Increment Counter",
            button_type="primary",
            icon="add",
            on_click=self._increment_counter,
            styles={"margin": "10px"}
        )
        
        self._reset_button = pmui.Button(
            name="Reset",
            button_type="secondary", 
            variant="outlined",
            icon="refresh",
            on_click=self._reset_counter,
            styles={"margin": "10px"}
        )
        
        self._text_input = pmui.TextInput.from_param(
            self.param.user_input,
            name="Text Input",
            placeholder="Enter some text...",
            styles={"margin": "10px 0"}
        )
        
        self._select_widget = pmui.Select.from_param(
            self.param.selected_option,
            name="Select Option",
            styles={"margin": "10px 0"}
        )
        
        self._status_card = pmui.Paper(*[
            pmui.Typography("Application Status", variant="h6"),
            pmui.Typography(object=self.status_display, variant="body1")
        ], styles={"padding": "20px", "margin": "20px 0"})
    
    def _create_layout(self):
        """Create the main application layout."""
        
        # Header section
        header = pmui.Paper(*[
            pmui.Typography(
                "🚀 Quick Start with Siemens iX", 
                variant="h4",
                styles={"textAlign": "center", "marginBottom": "10px"}
            ),
            pmui.Typography(
                "This app demonstrates the configure() function for instant Siemens iX branding.",
                variant="body1",
                styles={"textAlign": "center", "marginBottom": "0"}
            )
        ], styles={"padding": "30px", "marginBottom": "20px"})
        
        # Controls section
        controls = pmui.Paper(*[
            pmui.Typography("Interactive Controls", variant="h6", styles={"marginBottom": "15px"}),
            self._counter_display,
            pmui.Row(*[self._increment_button, self._reset_button]),
            self._text_input,
            self._select_widget
        ], styles={"padding": "20px", "marginBottom": "20px"})
        
        # Main layout using Container for proper centering
        self._layout = pmui.Container(*[
            header,
            controls,
            self._status_card
        ])  # Material UI responsive breakpoint
    
    @param.depends("counter")
    def counter_display(self):
        """Reactive display for the counter value."""
        return f"Counter: {self.counter}"
    
    @param.depends("user_input", "selected_option", "counter")
    def status_display(self):
        """Reactive status display showing current application state."""
        status_parts = [
            f"• Counter value: {self.counter}",
            f"• Text input: '{self.user_input}' ({len(self.user_input)} characters)",
            f"• Selected option: {self.selected_option}"
        ]
        return "\n".join(status_parts)
    
    def _increment_counter(self, event):
        """Increment the counter value."""
        self.counter += 1
    
    def _reset_counter(self, event):
        """Reset counter and clear inputs."""
        self.counter = 0
        self.user_input = ""
        self.selected_option = "Option 1"
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """
        Create a servable app with Siemens iX branding.
        
        Notice how simple this is with configure() - no manual theme setup required!
        """
        instance = cls(**params)
        
        # Create Page - themes are automatically configured by configure()
        page = pmui.Page(
            title="Quick Start - Siemens iX",
            main=[instance],
            sidebar=[
                pmui.Typography("Welcome!", variant="h6"),
                pmui.Typography(
                    "This sidebar shows the Siemens iX branding applied automatically.",
                    variant="body2",
                    styles={"marginBottom": "20px"}
                ),
                pmui.Alert(
                    object="✨ The configure() function handles all theming, logos, and defaults!",
                    alert_type="info"
                )
            ],
            # Theme toggle is enabled by default with configure()
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension()

# 🎯 This is the key line - configure() sets up everything!
# It applies:
# - Light and dark themes with Siemens iX colors
# - Siemens logos and favicon  
# - Component defaults and styling
# - Typography settings
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python quick_start.py`
    QuickStartApp.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve quick_start.py --port 5007 --dev --show`
    QuickStartApp.create_app().servable()