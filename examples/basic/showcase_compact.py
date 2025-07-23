"""
Compact Component Showcase - Siemens iX

A concise showcase of the most important Material UI components with
Siemens iX theming, designed to fit on screen without scrolling.
Perfect for screenshots and quick demonstrations.

Run with:
    panel serve showcase_compact.py --dev --show
Or:
    python showcase_compact.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import pandas as pd
import numpy as np
import hvplot.pandas
import time
import asyncio
from panel_siemens_ix import configure


class CompactShowcase(pn.viewable.Viewer):
    """
    Compact showcase displaying key components without scrolling.

    This example demonstrates the most commonly used Material UI components
    in a layout optimized for screenshots and quick demos.
    """

    # Sample parameters for interactive components
    text_value = param.String(default="Hello Siemens iX", doc="Sample text")
    number_value = param.Number(default=75, bounds=(0, 100), doc="Sample number")
    toggle_value = param.Boolean(default=True, doc="Sample toggle")
    select_value = param.Selector(
        default="Primary",
        objects=["Primary", "Secondary", "Success"],
        doc="Sample selection",
    )

    # Progress and busy indicator parameters
    progress_value = param.Number(default=0, bounds=(0, 100), doc="Progress counter")
    is_busy = param.Boolean(default=False, doc="Busy indicator state")
    counter_running = param.Boolean(default=False, doc="Counter running state")

    def __init__(self, **params):
        super().__init__(**params)

        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_layout()

    def _generate_sample_data(self):
        """Generate sample data for hvplot chart."""
        dates = pd.date_range("2024-01-01", periods=30, freq="D")
        values = np.cumsum(np.random.randn(30)) + 100
        efficiency = (
            85 + 10 * np.sin(np.linspace(0, 4 * np.pi, 30)) + np.random.randn(30) * 2
        )

        return pd.DataFrame(
            {
                "Date": dates,
                "Production": values,
                "Efficiency": efficiency.clip(70, 100),
            }
        )

    async def _start_progress_counter(self, event):
        """Start the progress counter with time.sleep simulation."""
        if self.counter_running:
            return

        self.counter_running = True
        self.progress_value = 0

        for i in range(101):
            if not self.counter_running:  # Allow stopping
                break
            self.progress_value = i
            await asyncio.sleep(0.05)  # 50ms delay for smooth animation

        self.counter_running = False

    async def _start_busy_operation(self, event):
        """Start a busy operation with time.sleep simulation."""
        if self.is_busy:
            return

        self.is_busy = True

        # Simulate some work with sleep
        await asyncio.sleep(3.0)  # 3 second operation

        self.is_busy = False

    def _stop_progress_counter(self, event):
        """Stop the progress counter."""
        self.counter_running = False

    def _create_layout(self):
        """Create compact layout showcasing key components."""

        # Header section
        header = pmui.Paper(
            pmui.Typography(
                "🎛️ Siemens iX Component Showcase",
                variant="h5",
                styles={"textAlign": "center", "marginBottom": "10px"},
            ),
            pmui.Typography(
                "Key Material UI components with Siemens iX theming",
                variant="body2",
                styles={"textAlign": "center", "color": "text.secondary"},
            ),
            styles={"padding": "20px", "marginBottom": "15px"},
        )

        # Button showcase
        buttons_section = pmui.Card(
            pmui.Typography("Buttons", variant="h6", styles={"marginBottom": "10px"}),
            pmui.Row(
                pmui.Button(
                    name="Primary",
                    button_type="primary",
                    icon="check_circle",
                    styles={"margin": "4px"},
                ),
                pmui.Button(
                    name="Secondary",
                    button_type="secondary",
                    icon="favorite",
                    styles={"margin": "4px"},
                ),
                pmui.Button(
                    name="Success",
                    button_type="success",
                    icon="check",
                    styles={"margin": "4px"},
                ),
                pmui.Button(
                    name="Warning",
                    button_type="warning",
                    icon="warning",
                    styles={"margin": "4px"},
                ),
                styles={"justifyContent": "center"},
            ),
            styles={"padding": "15px", "margin": "8px"},
        )

        # Input components
        inputs_section = pmui.Card(
            pmui.Typography("Inputs", variant="h6", styles={"marginBottom": "10px"}),
            pmui.Row(
                pmui.TextInput.from_param(
                    self.param.text_value,
                    name="Text Input",
                    styles={"flex": "1", "margin": "4px"},
                ),
                pmui.FloatInput.from_param(
                    self.param.number_value,
                    name="Number",
                    styles={"flex": "1", "margin": "4px"},
                ),
            ),
            pmui.Row(
                pmui.Select.from_param(
                    self.param.select_value,
                    name="Select",
                    styles={"flex": "1", "margin": "4px"},
                ),
                pmui.Switch.from_param(
                    self.param.toggle_value,
                    name="Switch",
                    styles={"flex": "1", "margin": "4px"},
                ),
            ),
            styles={"padding": "15px", "margin": "8px"},
        )

        # Progress and Busy Indicators
        progress_section = pmui.Card(
            pmui.Typography(
                "Progress & Busy Indicators",
                variant="h6",
                styles={"marginBottom": "10px"},
            ),
            pmui.Column(
                pmui.Row(
                    pmui.Button(
                        name="Start Counter",
                        button_type="primary",
                        icon="play_arrow",
                        on_click=self._start_progress_counter,
                        disabled=pn.bind(lambda x: x, self.param.counter_running),
                        styles={"margin": "4px"},
                    ),
                    pmui.Button(
                        name="Stop Counter",
                        button_type="secondary",
                        icon="stop",
                        on_click=self._stop_progress_counter,
                        disabled=pn.bind(lambda x: not x, self.param.counter_running),
                        styles={"margin": "4px"},
                    ),
                ),
                pmui.Column(
                    pmui.LinearProgress(
                        value=self.param.progress_value,
                        color="primary",
                        styles={"margin": "8px 0"},
                        visible=pn.bind(lambda x: x, self.param.counter_running),
                        width=320,
                    ),
                    pmui.Typography(
                        object=pn.bind(
                            lambda x: f"Counter: {x:.0f}%", self.param.progress_value
                        ),
                        variant="caption",
                    ),
                    styles={"flex": "1", "margin": "4px"},
                ),
                pmui.Column(
                    pmui.Button(
                        name="Busy Task",
                        button_type="warning",
                        icon="hourglass_empty"
                        if not self.is_busy
                        else "hourglass_full",
                        on_click=self._start_busy_operation,
                        disabled=pn.bind(lambda x: x, self.param.is_busy),
                        styles={"margin": "4px"},
                    ),
                    pmui.CircularProgress(
                        value=50,
                        color="warning",
                        size=40,
                        visible=pn.bind(lambda x: x, self.param.is_busy),
                        styles={"alignSelf": "center"},
                    ),
                    pmui.Typography(
                        object=pn.bind(
                            lambda x: "Working..." if x else "Ready", self.param.is_busy
                        ),
                        variant="caption",
                        styles={"textAlign": "center"},
                    ),
                    styles={
                        "flex": "0 0 auto",
                        "alignItems": "center",
                        "margin": "4px",
                    },
                ),
            ),
            styles={"padding": "15px", "margin": "8px"},
        )

        # Chart section with hvplot
        chart_section = pmui.Card(
            pmui.Typography(
                "Data Visualization", variant="h6", styles={"marginBottom": "10px"}
            ),
            self._create_chart(),
            styles={"padding": "15px", "margin": "8px", "height": "300px"},
        )

        # Chips and status indicators
        status_section = pmui.Card(
            pmui.Typography(
                "Status & Chips", variant="h6", styles={"marginBottom": "10px"}
            ),
            pmui.Row(
                pmui.Chip(object="Active", color="success", styles={"margin": "3px"}),
                pmui.Chip(object="Pending", color="warning", styles={"margin": "3px"}),
                pmui.Chip(object="Error", color="error", styles={"margin": "3px"}),
                pmui.Chip(object="Info", color="info", styles={"margin": "3px"}),
                styles={"justifyContent": "center", "flexWrap": "wrap"},
            ),
            pmui.Typography(
                object=self.status_display,
                variant="body2",
                styles={
                    "marginTop": "10px",
                    "textAlign": "center",
                    "color": "text.secondary",
                },
            ),
            styles={"padding": "15px", "margin": "8px"},
        )

        # Main layout - optimized for no scrolling
        content_grid = pmui.Row(
            pmui.Column(
                buttons_section, inputs_section, progress_section, styles={"flex": "1"}
            ),
            pmui.Column(chart_section, status_section, styles={"flex": "1"}),
        )

        self._layout = pmui.Container(
            header,
            content_grid,
            width_option="lg",
            styles={"maxHeight": "90vh", "overflow": "hidden"},
        )

    def _create_chart(self):
        """Create a simple hvplot chart."""
        try:
            data = self._generate_sample_data()
            chart = data.hvplot.line(
                x="Date",
                y="Production",
                title="Production Trend",
                height=250,
                width=450,
                color="#1976d2",  # Siemens primary color
                line_width=2,
            )
            return chart
        except Exception:
            # Fallback if hvplot fails
            return pmui.Typography(
                "📊 Chart placeholder - hvplot not available",
                variant="body2",
                styles={"textAlign": "center", "color": "text.secondary"},
            )

    @param.depends("text_value", "number_value", "toggle_value", "select_value")
    def status_display(self):
        """Display current component values."""
        return f"Values: '{self.text_value}' | {self.number_value:.0f} | {self.select_value} | {'On' if self.toggle_value else 'Off'}"

    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout

    @classmethod
    def create_app(cls, **params):
        """Create a servable compact showcase app."""
        instance = cls(**params)

        # Simple sidebar with key information
        sidebar_content = pmui.Column(
            pmui.Typography("Siemens iX", variant="h6"),
            pmui.Typography(
                "This showcase demonstrates key Material UI components with Siemens iX theming.",
                variant="body2",
                styles={"marginBottom": "15px"},
            ),
            pmui.Alert(
                object="💡 Use the theme toggle to switch between light and dark modes",
                alert_type="info",
            ),
            pmui.DatePicker(
                name="Select Date",
                styles={"marginTop": "10px", "width": "100%"},
            ),
            pmui.RadioBoxGroup(
                name="Options",
                options=["Option 1", "Option 2", "Option 3"],
                styles={"marginTop": "10px"},
            ),
            pmui.Checkbox(
                name="Agree to Terms",
                styles={"marginTop": "10px"},
            ),)
            

        page = pmui.Page(
            title="Compact Showcase - Siemens iX",
            main=[instance],
            sidebar=[sidebar_content],
            theme_toggle=True,
        )

        return page


# Enable Panel extensions (including hvplot support)
pn.extension("bokeh")

# Apply Siemens iX configuration
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python showcase_compact.py`
    CompactShowcase.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve showcase_compact.py --port 5007 --dev --show`
    CompactShowcase.create_app().servable()
