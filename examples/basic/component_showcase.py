"""
Material UI Component Showcase with Siemens iX

This example demonstrates the most commonly used Material UI components
styled with the Siemens iX design system. It follows Panel best practices
with parameter-driven architecture and reactive updates.

Run with:
    panel serve component_showcase.py --dev --show
Or:
    python component_showcase.py
"""

import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix import configure
import datetime


class ComponentShowcase(pn.viewable.Viewer):
    """
    Comprehensive showcase of Material UI components with Siemens iX theming.
    
    This class demonstrates various widget types, layouts, and interaction patterns
    following Panel's parameter-driven architecture.
    """
    
    # Input parameters for reactive behavior
    text_input = param.String(default="Hello Siemens iX", doc="Text input field")
    number_input = param.Number(default=42, bounds=(0, 100), doc="Number input")
    slider_value = param.Integer(default=50, bounds=(0, 100), doc="Slider value")
    boolean_toggle = param.Boolean(default=True, doc="Boolean toggle switch")
    select_option = param.Selector(
        default="Primary",
        objects=["Primary", "Secondary", "Success", "Warning", "Error", "Info"],
        doc="Select dropdown option"
    )
    date_value = param.Date(default=datetime.date.today(), doc="Date picker value")
    multiselect_values = param.ListSelector(
        default=["Option 1", "Option 3"],
        objects=["Option 1", "Option 2", "Option 3", "Option 4"],
        doc="Multi-select values"
    )
    
    # Display state parameters
    notification_count = param.Integer(default=0, doc="Number of notifications sent")
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_sections()
            self._create_layout()
    
    def _create_sections(self):
        """Create different component demonstration sections."""
        self._button_section = self._create_button_section()
        self._input_section = self._create_input_section()
        self._selection_section = self._create_selection_section()
        self._feedback_section = self._create_feedback_section()
        self._layout_section = self._create_layout_section()
        self._status_section = self._create_status_section()
    
    def _create_button_section(self):
        """Create button components demonstration."""
        
        # Different button types
        button_variants = pmui.Row(
            pmui.Button(
                name="Primary",
                button_type="primary",
                icon="star",
                on_click=self._handle_button_click,
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Secondary",
                button_type="secondary", 
                icon="favorite",
                on_click=self._handle_button_click,
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Success",
                button_type="success",
                icon="check_circle",
                on_click=self._handle_button_click,
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Warning",
                button_type="warning",
                icon="warning",
                on_click=self._handle_button_click,
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Error",
                button_type="error",
                icon="error",
                on_click=self._handle_button_click,
                styles={"margin": "5px"}
            ),
            styles={"flexWrap": "wrap"}
        )
        
        # Different button styles
        button_styles = pmui.Row(
            pmui.Button(
                name="Contained",
                button_type="primary",
                variant="contained",
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Outlined",
                button_type="primary",  
                variant="outlined",
                styles={"margin": "5px"}
            ),
            pmui.Button(
                name="Text",
                button_type="primary",
                variant="text",
                styles={"margin": "5px"}
            )
        )
        
        # Floating Action Button
        fab_example = pmui.Fab(
            icon="add",
            color="primary",
            on_click=self._handle_fab_click,
            styles={"margin": "10px"}
        )
        
        return pmui.Card(
            pmui.Typography("Buttons & Actions", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography("Button Types:", variant="subtitle2", styles={"marginTop": "10px"}),
            button_variants,
            pmui.Typography("Button Styles:", variant="subtitle2", styles={"marginTop": "20px"}),
            button_styles,
            pmui.Typography("Floating Action Button:", variant="subtitle2", styles={"marginTop": "20px"}),
            fab_example,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_input_section(self):
        """Create input components demonstration."""
        
        # DO create widgets using .from_param method for reactive behavior
        text_widget = pmui.TextInput.from_param(
            self.param.text_input,
            name="Text Input",
            placeholder="Enter text here...",
            styles={"margin": "10px 0"}
        )
        
        number_widget = pmui.FloatInput.from_param(
            self.param.number_input,
            name="Number Input",
            styles={"margin": "10px 0"}
        )
        
        textarea_widget = pmui.TextAreaInput(
            name="Text Area",
            placeholder="Enter multiple lines of text...",
            value="This is a text area component.\nIt supports multiple lines.",
            styles={"margin": "10px 0"}
        )
        
        password_widget = pmui.PasswordInput(
            name="Password",
            placeholder="Enter password...",
            styles={"margin": "10px 0"}
        )
        
        date_widget = pmui.DatePicker.from_param(
            self.param.date_value,
            name="Date Picker",
            styles={"margin": "10px 0"}
        )
        
        return pmui.Card(
            pmui.Typography("Input Components", variant="h6", styles={"marginBottom": "15px"}),
            text_widget,
            number_widget,
            textarea_widget,
            password_widget,
            date_widget,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_selection_section(self):
        """Create selection components demonstration."""
        
        # Single selection components
        select_widget = pmui.Select.from_param(
            self.param.select_option,
            name="Select Dropdown",
            styles={"margin": "10px 0"}
        )
        
        radio_group = pmui.RadioButtonGroup(
            name="Radio Button Group",
            options=["Option A", "Option B", "Option C"],
            value="Option A",
            styles={"margin": "10px 0"}
        )
        
        # Multi-selection components  
        multiselect_widget = pmui.MultiSelect.from_param(
            self.param.multiselect_values,
            name="Multi Select",
            styles={"margin": "10px 0"}
        )
        
        checkbox_group = pmui.CheckBoxGroup(
            name="Checkbox Group",
            options=["Feature A", "Feature B", "Feature C"],
            value=["Feature A"],
            styles={"margin": "10px 0"}
        )
        
        # Toggle components
        switch_widget = pmui.Switch.from_param(
            self.param.boolean_toggle,
            name="Switch Toggle"
        )
        
        checkbox_widget = pmui.Checkbox(
            name="Single Checkbox",
            value=True
        )
        
        return pmui.Card(
            pmui.Typography("Selection Components", variant="h6", styles={"marginBottom": "15px"}),
            select_widget,
            radio_group,
            multiselect_widget,
            checkbox_group,
            pmui.Row(switch_widget, checkbox_widget, styles={"margin": "10px 0"}),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_feedback_section(self):
        """Create feedback and indicator components."""
        
        # Progress indicators
        linear_progress = pmui.LinearProgress(
            value=self.slider_value,
            color="primary",
            styles={"margin": "10px 0"}
        )
        
        circular_progress = pmui.CircularProgress(
            value=75,
            color="secondary",
            size=50
        )
        
        # Slider for controlling progress
        slider_widget = pmui.IntSlider.from_param(
            self.param.slider_value,
            name="Progress Control",
            styles={"margin": "10px 0"}
        )
        
        # Alert components
        alerts = pmui.Column(
            pmui.Alert(
                object="This is an info alert with Siemens iX styling!",
                alert_type="info",
                styles={"margin": "5px 0"}
            ),
            pmui.Alert(
                object="Success! Operation completed successfully.",
                alert_type="success",
                styles={"margin": "5px 0"}
            ),
            pmui.Alert(
                object="Warning: Please check your input.",
                alert_type="warning",
                styles={"margin": "5px 0"}
            )
        )
        
        return pmui.Card(
            pmui.Typography("Feedback Components", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography("Progress Indicators:", variant="subtitle2"),
            slider_widget,
            linear_progress,
            pmui.Row(
                pmui.Typography("Circular Progress:", variant="body2"),
                circular_progress,
                styles={"alignItems": "center", "margin": "10px 0"}
            ),
            pmui.Typography("Alerts:", variant="subtitle2", styles={"marginTop": "20px"}),
            alerts,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_layout_section(self):
        """Create layout components demonstration."""
        
        # Tabs example
        tab_content = pmui.Tabs(
            ("Tab 1", pmui.Typography("Content of Tab 1 with Siemens iX styling")),
            ("Tab 2", pmui.Typography("Content of Tab 2 - tabs adapt to theme automatically")),
            ("Tab 3", pmui.Typography("Content of Tab 3 - notice the consistent styling"))
        )

        # Accordion example
        accordion_content = pmui.Accordion(
            ("Section 1", pmui.Typography("Accordion content adapts to Siemens iX theme colors and typography.")),
            ("Section 2", pmui.Typography("Each section can contain any Panel component with proper theming.")),
            ("Section 3", pmui.Typography("Collapsible sections are perfect for organizing complex interfaces."))
        )
        
        # Paper (elevated surface) examples
        paper_examples = pmui.Row(
            pmui.Paper(
                pmui.Typography("Paper Component", variant="h6"),
                pmui.Typography("Creates elevated surfaces", variant="body2"),
                styles={"padding": "15px", "margin": "5px", "flex": "1"}
            ),
            pmui.Paper(
                pmui.Typography("Another Paper", variant="h6"),
                pmui.Typography("With consistent elevation", variant="body2"),
                styles={"padding": "15px", "margin": "5px", "flex": "1"}
            )
        )
        
        return pmui.Card(
            pmui.Typography("Layout Components", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography("Tabs:", variant="subtitle2"),
            tab_content,
            pmui.Typography("Accordion:", variant="subtitle2", styles={"marginTop": "20px"}),
            accordion_content,
            pmui.Typography("Paper Components:", variant="subtitle2", styles={"marginTop": "20px"}),
            paper_examples,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_status_section(self):
        """Create status display section showing reactive updates."""
        return pmui.Card(
            pmui.Typography("Reactive Status Display", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(object=self.status_display, variant="body1"),
            pmui.Typography(
                f"Notifications sent: {self.notification_count}",
                variant="body2",
                styles={"marginTop": "10px"}
            ),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_layout(self):
        """Create the main application layout."""
        
        # Header
        header = pmui.Paper(
            pmui.Typography(
                "🎛️ Material UI Component Showcase",
                variant="h4", 
                styles={"textAlign": "center", "marginBottom": "10px"}
            ),
            pmui.Typography(
                "Comprehensive demonstration of Material UI components with Siemens iX theming",
                variant="body1",
                styles={"textAlign": "center"}
            ),
            styles={"padding": "30px", "marginBottom": "20px"}
        )
        
        # Main content container
        self._layout = pmui.Container(
            header,
            self._button_section,
            self._input_section,
            self._selection_section,
            self._feedback_section,
            self._layout_section,
            self._status_section,
            width_option="xl"  # Extra large responsive breakpoint
        )
    
    @param.depends(
        "text_input", "number_input", "slider_value", 
        "boolean_toggle", "select_option", "date_value"
    )
    def status_display(self):
        """Reactive status display showing current parameter values."""
        return f"""Current Values:
• Text: "{self.text_input}" ({len(self.text_input)} chars)
• Number: {self.number_input}
• Slider: {self.slider_value}%
• Toggle: {"On" if self.boolean_toggle else "Off"}
• Selection: {self.select_option}
• Date: {self.date_value.strftime("%Y-%m-%d")}"""
    
    def _handle_button_click(self, event):
        """Handle button click events with notifications."""
        self.notification_count += 1
        # Show notification (requires pn.extension(notifications=True))
        if hasattr(pn.state, 'notifications'):
            pn.state.notifications.info(
                f"'{event.obj.name}' button clicked! ({self.notification_count} total clicks)",
                duration=3000
            )
    
    def _handle_fab_click(self, event):
        """Handle floating action button clicks."""
        self.notification_count += 1
        if hasattr(pn.state, 'notifications'):
            pn.state.notifications.success(
                f"FAB clicked! Total: {self.notification_count}",
                duration=2000
            )
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """Create a servable app showcasing Material UI components."""
        instance = cls(**params)
        
        # Create Page with comprehensive sidebar
        page = pmui.Page(
            title="Component Showcase - Siemens iX",
            main=[instance],
            sidebar=[
                pmui.Typography("Component Guide", variant="h6"),
                pmui.Typography(
                    "This showcase demonstrates Material UI components styled with the Siemens iX design system.",
                    variant="body2",
                    styles={"marginBottom": "20px"}
                ),
                pmui.Accordion(
                    ("Buttons", pmui.Typography("Various button types, styles, and interactive elements including FAB components.")),
                    ("Inputs", pmui.Typography("Text inputs, number inputs, date pickers, and text areas with proper validation.")),
                    ("Selection", pmui.Typography("Dropdowns, radio buttons, checkboxes, and multi-select components.")),
                    ("Feedback", pmui.Typography("Progress indicators, alerts, and user feedback components.")),
                    ("Layouts", pmui.Typography("Tabs, accordions, papers and container components for organizing content."))
                ),
                pmui.Alert(
                    object="💡 All components automatically adapt to light/dark themes!",
                    alert_type="info",
                    styles={"marginTop": "20px"}
                )
            ],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions including notifications
pn.extension(notifications=True)

# Apply Siemens iX configuration
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python component_showcase.py`
    ComponentShowcase.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve component_showcase.py --port 5007 --dev --show`
    ComponentShowcase.create_app().servable()