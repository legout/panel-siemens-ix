"""
Minimal Panel Siemens iX Application

This is the simplest possible working example demonstrating how to create a
Panel application with Siemens iX theming. This example follows Panel best
practices with parameter-driven architecture.

Run with:
    panel serve minimal_app.py --dev --show
Or:
    python minimal_app.py
"""

import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme


class MinimalApp(pn.viewable.Viewer):
    """
    Minimal Siemens iX application demonstrating basic theming.
    
    This class follows Panel's parameter-driven architecture pattern,
    making it easily extensible and testable.
    """
    
    message = param.String(default="Hello, Siemens iX!", doc="Message to display")
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            # Create components with static layout + reactive content
            self._message_pane = pmui.Typography(
                object=self.message_display,
                variant="h4",
                styles={"textAlign": "center", "padding": "20px"}
            )
            
            self._button = pmui.Button(
                name="Click me!",
                button_type="primary",
                on_click=self._handle_click,
                styles={"marginTop": "20px"}
            )
            
            # Create main layout
            self._layout = pmui.Container(
                self._message_pane,
                self._button
            )
    
    @param.depends("message")
    def message_display(self):
        """Reactive method to update message display."""
        return f"🚀 {self.message}"
    
    def _handle_click(self, event):
        """Handle button click events."""
        self.message = "Button clicked! Welcome to Siemens iX with Panel!"
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod 
    def create_app(cls, **params):
        """
        Create a servable app with proper Page template.
        
        This method demonstrates the recommended way to create Panel applications
        with Material UI theming.
        """
        instance = cls(**params)
        
        # Create Page with Siemens iX theme configuration
        page = pmui.Page(
            title="Minimal Siemens iX App",
            # DO provide theme configuration for both light and dark modes
            theme_config={
                "light": siemens_ix_light_theme,
                "dark": siemens_ix_dark_theme
            },
            # DO provide content in the main area
            main=[instance],
            # DO include theme toggle for better UX
            theme_toggle=True
        )
        
        return page


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python minimal_app.py`
    MinimalApp.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve minimal_app.py --port 5007 --dev --show`
    MinimalApp.create_app().servable()