"""
Siemens iX Chart Colors Demo

This example demonstrates the use of improved Siemens iX color palettes
for data visualization with hvPlot and Plotly. It showcases:

- Continuous colormaps for sequential data
- Categorical palettes for discrete categories
- Theme-optimized colors for light and dark modes
- Integration patterns with popular plotting libraries

Run with:
    panel serve chart_colors_demo.py --dev --show
Or:
    python chart_colors_demo.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import pandas as pd
import numpy as np
import datetime
from typing import List

# Import Siemens iX components
from panel_siemens_ix import configure
from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme
from panel_siemens_ix.colors import (
    get_colors,
    get_continuous_cmap,
    get_categorical_palette,
)

# Try to import plotting libraries
try:
    import hvplot.pandas
    _HVPLOT_AVAILABLE = True
except ImportError:
    _HVPLOT_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    _PLOTLY_AVAILABLE = True
except ImportError:
    _PLOTLY_AVAILABLE = False


# Configure Panel extensions
pn.extension(sizing_mode="stretch_width")


# Data Generation Functions
@pn.cache(max_items=5, ttl=300)
def generate_time_series_data(
    n_points: int = 100,
    n_series: int = 3,
    trend: bool = True
) -> pd.DataFrame:
    """Generate synthetic time series data for demonstration."""
    np.random.seed(42)

    dates = pd.date_range(
        end=datetime.date.today(),
        periods=n_points,
        freq='D'
    )

    data = []
    for i in range(n_series):
        base = np.random.normal(100 * (i + 1), 10, n_points)
        if trend:
            trend_component = np.linspace(0, 20, n_points) * (i + 1)
            base += trend_component

        # Add seasonality
        seasonal = 5 * np.sin(2 * np.pi * np.arange(n_points) / (n_points / 4))
        base += seasonal

        # Add noise
        noise = np.random.normal(0, 2, n_points)
        values = base + noise

        data.append(pd.DataFrame({
            'date': dates,
            'value': values,
            'series': f'Series {i+1}',
            'category': chr(65 + i)  # A, B, C, ...
        }))

    return pd.concat(data, ignore_index=True)


@pn.cache(max_items=5, ttl=300)
def generate_scatter_data(
    n_points: int = 200,
    n_categories: int = 5
) -> pd.DataFrame:
    """Generate synthetic scatter plot data with categories."""
    np.random.seed(42)

    data = []
    for i in range(n_categories):
        # Generate clusters
        n_cluster = n_points // n_categories
        center_x = np.random.uniform(-10, 10)
        center_y = np.random.uniform(-10, 10)

        x = np.random.normal(center_x, 2, n_cluster)
        y = np.random.normal(center_y, 2, n_cluster)
        z = np.random.normal(i * 10, 5, n_cluster)  # Third dimension

        data.append(pd.DataFrame({
            'x': x,
            'y': y,
            'z': z,
            'category': f'Category {i+1}',
            'size': np.random.uniform(10, 100, n_cluster)
        }))

    return pd.concat(data, ignore_index=True)


@pn.cache(max_items=3, ttl=300)
def generate_heatmap_data(
    size: int = 20
) -> pd.DataFrame:
    """Generate synthetic heatmap data."""
    np.random.seed(42)

    # Create correlation-like matrix
    base = np.random.normal(0, 1, (size, size))
    # Make it symmetric
    matrix = (base + base.T) / 2
    # Add some structure
    for i in range(size):
        for j in range(size):
            matrix[i, j] += np.exp(-((i - size//2)**2 + (j - size//2)**2) / (size**2 / 4))

    # Convert to long format
    rows, cols = np.triu_indices_from(matrix)
    df = pd.DataFrame({
        'row': rows,
        'col': cols,
        'value': matrix[rows, cols]
    })

    return df


@pn.cache(max_items=3, ttl=300)
def generate_categorical_data(
    n_categories: int = 8
) -> pd.DataFrame:
    """Generate categorical data for bar charts."""
    np.random.seed(42)

    categories = [f'Category {i+1}' for i in range(n_categories)]
    values = np.random.randint(10, 100, n_categories)

    # Add some groups
    groups = ['Group A'] * (n_categories // 2) + ['Group B'] * (n_categories - n_categories // 2)

    return pd.DataFrame({
        'category': categories,
        'value': values,
        'group': groups[:n_categories]
    })


class ChartColorsDemo(pn.viewable.Viewer):
    """
    Interactive demonstration of Siemens iX color palettes for data visualization.
    """

    # Parameters for interactive exploration
    current_theme = param.Selector(
        default="light",
        objects=["light", "dark"],
        doc="Current theme mode"
    )
    chart_library = param.Selector(
        default="hvplot",
        objects=["hvplot", "plotly", "both"],
        doc="Chart library to use"
    )
    n_categories = param.Integer(
        default=5,
        bounds=(2, 12),
        doc="Number of categories for demonstration"
    )
    chart_type = param.Selector(
        default="line",
        objects=["line", "scatter", "bar", "heatmap", "area"],
        doc="Type of chart to display"
    )
    show_continuous = param.Boolean(
        default=True,
        doc="Show continuous colormap examples"
    )
    show_categorical = param.Boolean(
        default=True,
        doc="Show categorical palette examples"
    )

    def __init__(self, **params):
        super().__init__(**params)

        # Initialize the theme
        self._update_theme()

    @param.depends('current_theme', watch=True)
    def _update_theme(self):
        """Update the theme when changed."""
        # Set the default theme configuration
        pmui.Page.param.theme_config.default = dict(
            light=siemens_ix_light_theme,
            dark=siemens_ix_dark_theme
        )
        # Note: The actual theme switching is handled by the Page component
        # This method could be used to trigger updates if needed

    @param.depends('chart_library', 'chart_type', 'n_categories',
                   'show_continuous', 'show_categorical', 'current_theme')
    def charts_panel(self):
        """Create the main charts display panel."""
        charts = []

        # Title
        charts.append(
            pmui.Typography(
                f"📊 Siemens iX Chart Colors Demo - {self.chart_library.title()}",
                variant="h4",
                styles={"marginBottom": "20px"}
            )
        )

        # Continuous colormap demo
        if self.show_continuous:
            charts.extend(self._create_continuous_demo())

        # Categorical palette demo
        if self.show_categorical:
            charts.extend(self._create_categorical_demo())

        # Specific chart type demos
        if self.chart_type == "line":
            charts.extend(self._create_line_charts())
        elif self.chart_type == "scatter":
            charts.extend(self._create_scatter_charts())
        elif self.chart_type == "bar":
            charts.extend(self._create_bar_charts())
        elif self.chart_type == "heatmap":
            charts.extend(self._create_heatmap_charts())
        elif self.chart_type == "area":
            charts.extend(self._create_area_charts())

        return pn.GridBox(
            *charts,
            ncols=1
        )

    def _create_continuous_demo(self):
        """Create continuous colormap demonstration."""
        components = []

        components.append(
            pmui.Typography(
                "Continuous Colormap",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Get current colors
        colors = get_colors(self.current_theme)

        # Create a simple gradient visualization
        n_colors = 128
        cmap = get_continuous_cmap(
            dark_theme=(self.current_theme == "dark"),
            n_colors=n_colors
        )

        # Create gradient visualization
        gradient_html = f"""
        <div style="
            width: 100%;
            height: 40px;
            background: linear-gradient(to right, {', '.join(cmap[::max(1, n_colors//20)])});
            border: 1px solid {colors.border['std']};
            border-radius: 4px;
            margin-bottom: 10px;
        "></div>
        """

        components.append(pn.pane.HTML(gradient_html))

        # Add color samples
        color_samples = []
        for i in [0, n_colors//4, n_colors//2, 3*n_colors//4, n_colors-1]:
            color_samples.append(
                pmui.Paper(
                    pmui.Typography(cmap[i], variant="caption", styles={"fontFamily": "monospace"}),
                    elevation=0,
                    styles={
                        "backgroundColor": cmap[i],
                        "color": "white" if self.current_theme == "dark" else "black",
                        "padding": "8px",
                        "borderRadius": "4px",
                        "textAlign": "center"
                    }
                )
            )

        components.append(
            pn.GridBox(*color_samples, ncols=5)
        )

        return components

    def _create_categorical_demo(self):
        """Create categorical palette demonstration."""
        components = []

        components.append(
            pmui.Typography(
                "Categorical Palette",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Get palette
        palette = get_categorical_palette(
            dark_theme=(self.current_theme == "dark"),
            n_colors=self.n_categories
        )

        # Create color swatches
        swatches = []
        for i, color in enumerate(palette):
            swatches.append(
                pmui.Paper(
                    pmui.Typography(
                        f"{i+1}",
                        variant="body2",
                        styles={"fontWeight": "bold"}
                    ),
                    pmui.Typography(
                        color,
                        variant="caption",
                        styles={"fontFamily": "monospace"}
                    ),
                    elevation=0,
                    styles={
                        "backgroundColor": color,
                        "color": self._get_text_color(color),
                        "padding": "12px",
                        "borderRadius": "4px",
                        "textAlign": "center",
                        "minHeight": "80px"
                    }
                )
            )

        components.append(
            pn.GridBox(*swatches, ncols=self.n_categories)
        )

        return components

    def _create_line_charts(self):
        """Create line chart examples."""
        components = []

        components.append(
            pmui.Typography(
                "Line Charts with Continuous Colormap",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Generate data
        data = generate_time_series_data(n_series=3)

        if self.chart_library in ["hvplot", "both"] and _HVPLOT_AVAILABLE:
            # hvPlot line chart
            cmap = get_continuous_cmap(dark_theme=(self.current_theme == "dark"))

            chart = data.hvplot.line(
                x='date',
                y='value',
                by='series',
                cmap=cmap[:3],
                line_width=2,
                height=300,
                responsive=True
            )

            components.append(pn.pane.HoloViews(chart))

        if self.chart_library in ["plotly", "both"] and _PLOTLY_AVAILABLE:
            # Plotly line chart
            fig = go.Figure()
            colors = get_colors(self.current_theme)

            for i, series in enumerate(data['series'].unique()):
                series_data = data[data['series'] == series]
                palette = get_categorical_palette(
                    dark_theme=(self.current_theme == "dark"),
                    n_colors=3
                )

                fig.add_trace(go.Scatter(
                    x=series_data['date'],
                    y=series_data['value'],
                    name=series,
                    line=dict(color=palette[i], width=2)
                ))

            fig.update_layout(
                height=300,
                showlegend=True,
                plot_bgcolor=colors.background['paper'],
                paper_bgcolor=colors.background['default'],
                font=dict(color=colors.text['primary'])
            )

            components.append(pn.pane.Plotly(fig))

        return components

    def _create_scatter_charts(self):
        """Create scatter plot examples."""
        components = []

        components.append(
            pmui.Typography(
                "Scatter Plots with Categorical Colors",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Generate data
        data = generate_scatter_data(n_categories=self.n_categories)

        if self.chart_library in ["hvplot", "both"] and _HVPLOT_AVAILABLE:
            # hvPlot scatter
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=self.n_categories
            )

            chart = data.hvplot.scatter(
                x='x',
                y='y',
                by='category',
                cmap=palette,
                size='size',
                alpha=0.7,
                height=400,
                responsive=True
            )

            components.append(pn.pane.HoloViews(chart))

        if self.chart_library in ["plotly", "both"] and _PLOTLY_AVAILABLE:
            # Plotly scatter
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=self.n_categories
            )
            colors = get_colors(self.current_theme)

            fig = px.scatter(
                data,
                x='x',
                y='y',
                color='category',
                size='size',
                color_discrete_sequence=palette,
                height=400
            )

            fig.update_layout(
                plot_bgcolor=colors.background['paper'],
                paper_bgcolor=colors.background['default'],
                font=dict(color=colors.text['primary'])
            )

            components.append(pn.pane.Plotly(fig))

        return components

    def _create_bar_charts(self):
        """Create bar chart examples."""
        components = []

        components.append(
            pmui.Typography(
                "Bar Charts with Custom Palettes",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Generate data
        data = generate_categorical_data(n_categories=self.n_categories)

        if self.chart_library in ["hvplot", "both"] and _HVPLOT_AVAILABLE:
            # hvPlot bar chart
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=self.n_categories
            )

            chart = data.hvplot.bar(
                x='category',
                y='value',
                cmap=palette,
                height=300,
                responsive=True
            )

            components.append(pn.pane.HoloViews(chart))

        if self.chart_library in ["plotly", "both"] and _PLOTLY_AVAILABLE:
            # Plotly bar chart
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=self.n_categories
            )
            colors = get_colors(self.current_theme)

            fig = px.bar(
                data,
                x='category',
                y='value',
                color='category',
                color_discrete_sequence=palette,
                height=300
            )

            fig.update_layout(
                plot_bgcolor=colors.background['paper'],
                paper_bgcolor=colors.background['default'],
                font=dict(color=colors.text['primary']),
                showlegend=False
            )

            components.append(pn.pane.Plotly(fig))

        return components

    def _create_heatmap_charts(self):
        """Create heatmap examples."""
        components = []

        components.append(
            pmui.Typography(
                "Heatmaps with Continuous Colormaps",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Generate data
        data = generate_heatmap_data(size=15)

        if self.chart_library in ["hvplot", "both"] and _HVPLOT_AVAILABLE:
            # hvPlot heatmap
            cmap = get_continuous_cmap(dark_theme=(self.current_theme == "dark"))

            # Pivot data for heatmap
            heatmap_data = data.pivot(index='row', columns='col', values='value')

            chart = heatmap_data.hvplot.heatmap(
                cmap=cmap,
                height=400,
                responsive=True
            )

            components.append(pn.pane.HoloViews(chart))

        if self.chart_library in ["plotly", "both"] and _PLOTLY_AVAILABLE:
            # Plotly heatmap
            cmap = get_continuous_cmap(dark_theme=(self.current_theme == "dark"))
            colors = get_colors(self.current_theme)

            # Create custom colorscale for Plotly
            colorscale = []
            step = len(cmap) // 10
            for i in range(0, len(cmap), step):
                colorscale.append([i / len(cmap), cmap[i]])
            colorscale.append([1.0, cmap[-1]])

            fig = go.Figure(data=go.Heatmap(
                z=data.pivot(index='row', columns='col', values='value').values,
                colorscale=colorscale,
                showscale=True
            ))

            fig.update_layout(
                height=400,
                plot_bgcolor=colors.background['paper'],
                paper_bgcolor=colors.background['default'],
                font=dict(color=colors.text['primary'])
            )

            components.append(pn.pane.Plotly(fig))

        return components

    def _create_area_charts(self):
        """Create area chart examples."""
        components = []

        components.append(
            pmui.Typography(
                "Area Charts with Stacked Colors",
                variant="h6",
                styles={"marginBottom": "10px"}
            )
        )

        # Generate data
        data = generate_time_series_data(n_series=3, n_points=50)

        if self.chart_library in ["hvplot", "both"] and _HVPLOT_AVAILABLE:
            # hvPlot area chart
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=3,
                opacity=True
            )

            chart = data.hvplot.area(
                x='date',
                y='value',
                by='series',
                cmap=palette,
                alpha=0.7,
                stacked=True,
                height=300,
                responsive=True
            )

            components.append(pn.pane.HoloViews(chart))

        if self.chart_library in ["plotly", "both"] and _PLOTLY_AVAILABLE:
            # Plotly area chart
            palette = get_categorical_palette(
                dark_theme=(self.current_theme == "dark"),
                n_colors=3
            )
            colors = get_colors(self.current_theme)

            fig = go.Figure()

            for i, series in enumerate(data['series'].unique()):
                series_data = data[data['series'] == series]

                fig.add_trace(go.Scatter(
                    x=series_data['date'],
                    y=series_data['value'],
                    name=series,
                    fill='tonexty' if i > 0 else 'tozeroy',
                    line=dict(color=palette[i]),
                    stackgroup='one'
                ))

            fig.update_layout(
                height=300,
                plot_bgcolor=colors.background['paper'],
                paper_bgcolor=colors.background['default'],
                font=dict(color=colors.text['primary'])
            )

            components.append(pn.pane.Plotly(fig))

        return components

    def _get_text_color(self, bg_color: str) -> str:
        """Determine if white or black text has better contrast."""
        # Simple luminance calculation
        bg_color = bg_color.lstrip('#')
        r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return 'white' if luminance < 0.5 else 'black'

    def controls_panel(self):
        """Create the controls panel."""
        controls = [
            pmui.Typography("Chart Controls", variant="h6", styles={"marginBottom": "15px"}),

            pmui.Column(
                pmui.Select.from_param(
                    self.param.current_theme,
                    label="Theme"
                ),
                pmui.Select.from_param(
                    self.param.chart_library,
                    label="Chart Library"
                ),
                pmui.Select.from_param(
                    self.param.chart_type,
                    label="Chart Type"
                ),
                pmui.IntSlider.from_param(
                    self.param.n_categories,
                    label="Number of Categories"
                ),
            ),

            pmui.Divider(),

            pmui.Column(
                pmui.Switch.from_param(
                    self.param.show_continuous,
                    label="Show Continuous Colormap"
                ),
                pmui.Switch.from_param(
                    self.param.show_categorical,
                    label="Show Categorical Palette"
                ),
            ),
        ]

        return pmui.Card(*controls, title="Controls", elevation=2)

    def code_examples_panel(self):
        """Create code examples panel."""
        examples = [
            pmui.Typography("Code Examples", variant="h6", styles={"marginBottom": "15px"}),

            pmui.Card(
              pmui.Column(
                  pmui.Typography("Using Continuous Colormap", variant="subtitle1", styles={"marginBottom": "10px"}),
                  pmui.Typography(
                      """# Get continuous colormap for current theme
cmap = get_continuous_cmap(
    dark_theme=(theme == "dark"),
    n_colors=128
)

# Use with hvPlot
df.hvplot.line(cmap=cmap)

# Use with Plotly
fig = px.scatter(
    data,
    color_continuous_scale=cmap
)""",
                      variant="body2",
                      styles={"fontFamily": "monospace", "fontSize": "12px"}
                  )
              ),
              styles={"marginBottom": "10px"}
          ),

          pmui.Card(
              pmui.Column(
                  pmui.Typography("Using Categorical Palette", variant="subtitle1", styles={"marginBottom": "10px"}),
                  pmui.Typography(
                      """# Get categorical palette
palette = get_categorical_palette(
    dark_theme=(theme == "dark"),
    n_categories=5
)

# Use with hvPlot
df.hvplot.bar(by='category', cmap=palette)

# Use with Plotly
fig = px.bar(
    data,
    color='category',
    color_discrete_sequence=palette
)""",
                      variant="body2",
                      styles={"fontFamily": "monospace", "fontSize": "12px"}
                  )
              ),
              styles={"marginBottom": "10px"}
          ),

          pmui.Card(
              pmui.Column(
                  pmui.Typography("Theme Integration", variant="subtitle1", styles={"marginBottom": "10px"}),
                  pmui.Typography(
                      """# Configure Siemens iX theme
from panel_siemens_ix import configure

configure()

# Colors adapt automatically to theme
colors = get_colors("dark" if pn.state.theme == "dark" else "light")""",
                      variant="body2",
                      styles={"fontFamily": "monospace", "fontSize": "12px"}
                  )
              ),
              styles={"marginBottom": "10px"}
          ),
        ]

        return pmui.Card(*examples, title="Usage Examples", elevation=2)

    def __panel__(self):
        """Create the main panel layout."""
        # Create header
        header = pmui.Paper(
            pmui.Typography(
                "🎨 Siemens iX Chart Colors Demo",
                variant="h4",
                styles={"marginBottom": "10px"}
            ),
            pmui.Typography(
                "Interactive demonstration of improved color palettes for data visualization",
                variant="body1",
                styles={"marginBottom": "20px"}
            ),
            elevation=0,
            styles={"padding": "20px"}
        )

        # Main layout with sidebar
        sidebar = pmui.Paper(
            self.controls_panel(),
            self.code_examples_panel(),
            elevation=1,
            styles={"padding": "20px"}
        )

        main_content = pmui.Paper(
            self.charts_panel,
            elevation=1,
            styles={"padding": "20px"}
        )

        # Use responsive layout - simple column for all screen sizes
        layout = pmui.Column(
            header,
            pn.Row(
                pmui.Paper(sidebar, elevation=0, styles={"width": "300px", "marginRight": "20px"}),
                pmui.Paper(main_content, elevation=0, styles={"flex": "1"}),
            )
        )

        return layout

    @classmethod
    def create_app(cls, **params):
        """Create a servable app with theme switching capabilities."""
        instance = cls(**params)

        # Create Page with both theme configurations
        page = pmui.Page(
            title="Siemens iX Chart Colors Demo",
            theme_config={
                "light": siemens_ix_light_theme,
                "dark": siemens_ix_dark_theme
            },
            main=[instance],
            theme_toggle=True
        )

        return page


# Configure Panel extensions
pn.extension()

# Apply Siemens iX configuration
configure(with_logo=True)


# Create and serve the demo
if __name__ == "__main__":
    # Run with Python
    ChartColorsDemo.create_app().show(port=5007, open=True)

# For panel serve
elif pn.state.served:
    ChartColorsDemo.create_app().servable()