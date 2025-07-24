"""
Siemens iX Time Series Analytics Dashboard

This advanced example demonstrates a comprehensive data analytics dashboard featuring:
- Realistic sample dataset generation (environmental sensor readings)
- Interactive time series visualizations using hvPlot
- Parameter-driven architecture with pn.viewable.Viewer
- Material UI components with Siemens iX theming
- Dynamic exploration and analysis capabilities

Features:
- Realistic time series data generation for environmental sensors
- Interactive visualizations with hvPlot
- Dynamic parameter controls for filtering and aggregation
- KPI cards showing current, min, max, and average values
- Data table with recent readings
- Responsive Material UI design with Siemens iX theming

Run with:
    panel serve time_series_dashboard.py --dev --show
Or:
    python time_series_dashboard.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import pandas as pd
import numpy as np
import datetime
import hvplot.pandas  # noqa
from panel_siemens_ix import configure


# Generate realistic time series sensor data
def generate_sensor_data(days: int = 30, frequency: str = 'H') -> pd.DataFrame:
    """
    Generate realistic environmental sensor data for demonstration.
    
    Parameters
    ----------
    days : int, optional
        Number of days of data to generate (default is 30)
    frequency : str, optional
        Frequency of data points ('H' for hourly, 'T' for minutely, etc.)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with timestamp and sensor readings
    """
    # Create date range
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq=frequency)
    
    # Initialize random seed for reproducibility
    np.random.seed(42)
    
    # Base values for different sensors
    base_temp = 20  # Celsius
    base_humidity = 50  # Percentage
    base_pressure = 1013  # hPa
    base_co2 = 400  # ppm
    
    # Create realistic time series with trends, seasonality and noise
    n_points = len(dates)
    
    # Temperature with daily cycle and seasonal trend
    daily_temp_variation = 5 * np.sin(2 * np.pi * np.arange(n_points) / 24)  # Daily cycle
    seasonal_temp_trend = 2 * np.sin(2 * np.pi * np.arange(n_points) / (24 * 30))  # Monthly trend
    temp_noise = np.random.normal(0, 1, n_points)
    temperature = base_temp + daily_temp_variation + seasonal_temp_trend + temp_noise
    
    # Humidity with inverse relationship to temperature and daily cycle
    humidity_base = base_humidity - 0.5 * (temperature - base_temp)
    daily_humidity_variation = 10 * np.cos(2 * np.pi * np.arange(n_points) / 24)
    humidity_noise = np.random.normal(0, 2, n_points)
    humidity = humidity_base + daily_humidity_variation + humidity_noise
    humidity = np.clip(humidity, 10, 90)  # Realistic bounds
    
    # Pressure with slow variations
    pressure_trend = 10 * np.sin(2 * np.pi * np.arange(n_points) / (24 * 7))  # Weekly trend
    pressure_noise = np.random.normal(0, 5, n_points)
    pressure = base_pressure + pressure_trend + pressure_noise
    
    # CO2 with gradual increase and daily variations
    co2_trend = np.linspace(0, 20, n_points)  # Gradual increase
    daily_co2_variation = 50 * np.sin(2 * np.pi * np.arange(n_points) / 24)
    co2_noise = np.random.normal(0, 10, n_points)
    co2 = base_co2 + co2_trend + daily_co2_variation + co2_noise
    co2 = np.clip(co2, 300, 2000)  # Realistic bounds
    
    # Light intensity (lux) with strong daily cycle
    light_base = 500 + 500 * np.sin(2 * np.pi * np.arange(n_points) / 24 - np.pi/2)
    light_noise = np.random.normal(0, 50, n_points)
    light = np.maximum(0, light_base + light_noise)  # No negative light
    
    # Sound level (dB) with random variations around base
    sound_base = 45  # dB
    sound_variation = 10 * np.random.normal(0, 1, n_points)
    sound = sound_base + sound_variation
    sound = np.clip(sound, 20, 80)  # Realistic bounds
    
    # Create DataFrame
    data = pd.DataFrame({
        'timestamp': dates,
        'temperature_c': np.round(temperature, 2),
        'humidity_pct': np.round(humidity, 2),
        'pressure_hpa': np.round(pressure, 2),
        'co2_ppm': np.round(co2, 2),
        'light_lux': np.round(light, 2),
        'sound_db': np.round(sound, 2)
    })
    
    return data


class TimeSeriesDashboard(pn.viewable.Viewer):
    """
    Interactive time series analytics dashboard with realistic environmental data.
    
    This dashboard demonstrates advanced Panel features:
    - Parameter-driven architecture with reactive updates
    - Integration with hvPlot for interactive visualizations
    - Responsive Material UI design with Siemens iX theming
    - Dynamic data filtering and aggregation
    """
    
    # Dashboard parameters
    days = param.Integer(
        default=7, bounds=(1, 30),
        doc="Number of days of historical data to display"
    )
    
    frequency = param.Selector(
        default='H', objects=['H', '2H', '6H', 'D'],
        doc="Data aggregation frequency"
    )
    
    metric = param.Selector(
        default='temperature_c',
        objects=['temperature_c', 'humidity_pct', 'pressure_hpa', 'co2_ppm', 'light_lux', 'sound_db'],
        doc="Primary metric to visualize"
    )
    
    aggregation = param.Selector(
        default='mean',
        objects=['mean', 'median', 'min', 'max', 'std'],
        doc="Aggregation method for downsampling"
    )
    
    color = param.Color(
        default='#1976d2',
        doc="Color for the primary visualization"
    )
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # Generate initial dataset
        self.data = generate_sensor_data(days=30)
        
        # Configure sizing mode
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_components()
            self._create_layout()
    
    def _create_components(self):
        """Create dashboard components."""
        # Header
        self._header = pmui.Paper(
            pmui.Typography("🌡️ Environmental Sensor Analytics Dashboard", variant="h4"),
            pmui.Typography(
                "Interactive visualization of environmental sensor data with time series analysis",
                variant="subtitle1",
                styles={"color": "text.secondary"}
            ),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        # Control widgets
        self._control_widgets = self._create_control_widgets()
        
        # KPI cards
        self._kpi_section = self._create_kpi_section()
        
        # Main chart
        self._chart_section = self._create_chart_section()
        
        # Data table
        self._table_section = self._create_table_section()
    
    def _create_control_widgets(self):
        """Create control widgets for the sidebar."""
        days_widget = pmui.IntSlider.from_param(
            self.param.days,
            name="Time Range (days)",
            styles={"margin": "10px 0"}
        )
        
        frequency_widget = pmui.Select.from_param(
            self.param.frequency,
            name="Aggregation Frequency",
            styles={"margin": "10px 0"}
        )
        
        metric_widget = pmui.Select.from_param(
            self.param.metric,
            name="Metric",
            styles={"margin": "10px 0"}
        )
        
        aggregation_widget = pmui.Select.from_param(
            self.param.aggregation,
            name="Aggregation Method",
            styles={"margin": "10px 0"}
        )
        
        color_widget = pmui.ColorPicker.from_param(
            self.param.color,
            name="Chart Color",
            styles={"margin": "10px 0"}
        )
        
        return pmui.Column(
            pmui.Typography("🎛️ Dashboard Controls", variant="h6"),
            days_widget,
            frequency_widget,
            metric_widget,
            aggregation_widget,
            color_widget,
            pmui.Alert(
                object="💡 Adjust parameters to explore different aspects of the data",
                alert_type="info",
                styles={"marginTop": "20px"}
            ),
            styles={"padding": "20px"}
        )
    
    def _create_kpi_section(self):
        """Create KPI cards section."""
        def create_kpi_card(title, value_func, icon="", color="primary"):
            """Helper to create consistent KPI cards."""
            return pmui.Card(
                pmui.Row(
                    pmui.Column(
                        pmui.Typography(title, variant="subtitle2"),
                        pmui.Typography(object=value_func, variant="h6")
                    ),
                    pmui.Avatar(icon, styles={"backgroundColor": f"{color}.main"}) if icon else None,
                    styles={"justifyContent": "space-between", "alignItems": "center"}
                ),
                styles={"padding": "15px", "margin": "5px", "minHeight": "100px"}
            )
        
        # Create KPI cards
        kpi_cards = pmui.Row(
            create_kpi_card("Current Value", self.current_value, icon="speed", color="primary"),
            create_kpi_card("Min Value", self.min_value, icon="arrow_downward", color="info"),
            create_kpi_card("Max Value", self.max_value, icon="arrow_upward", color="warning"),
            create_kpi_card("Average", self.avg_value, icon="trending_flat", color="success"),
            styles={"flexWrap": "wrap"}
        )
        
        return pmui.Container(
            pmui.Typography("📊 Key Metrics", variant="h6", styles={"marginBottom": "15px"}),
            kpi_cards,
            styles={"marginBottom": "20px"}
        )
    
    # KPI value methods
    @param.depends("metric", "days")
    def current_value(self):
        """Get current value for the selected metric."""
        filtered_data = self.filtered_data
        if len(filtered_data) > 0:
            value = filtered_data[self.metric].iloc[-1]
            unit = self._get_unit_for_metric(self.metric)
            return f"{value:.2f} {unit}"
        return "N/A"
    
    @param.depends("metric", "days")
    def min_value(self):
        """Get minimum value for the selected metric."""
        filtered_data = self.filtered_data
        if len(filtered_data) > 0:
            value = filtered_data[self.metric].min()
            unit = self._get_unit_for_metric(self.metric)
            return f"{value:.2f} {unit}"
        return "N/A"
    
    @param.depends("metric", "days")
    def max_value(self):
        """Get maximum value for the selected metric."""
        filtered_data = self.filtered_data
        if len(filtered_data) > 0:
            value = filtered_data[self.metric].max()
            unit = self._get_unit_for_metric(self.metric)
            return f"{value:.2f} {unit}"
        return "N/A"
    
    @param.depends("metric", "days")
    def avg_value(self):
        """Get average value for the selected metric."""
        filtered_data = self.filtered_data
        if len(filtered_data) > 0:
            value = filtered_data[self.metric].mean()
            unit = self._get_unit_for_metric(self.metric)
            return f"{value:.2f} {unit}"
        return "N/A"
    
    def _create_chart_section(self):
        """Create the main chart section."""
        return pmui.Paper(
            pmui.Typography("📈 Time Series Visualization", variant="h6", styles={"marginBottom": "15px"}),
            # Chart will be added reactively
            self.time_series_plot,
            styles={"padding": "20px", "marginBottom": "20px", "minHeight": "400px"}
        )
    
    def _create_table_section(self):
        """Create data table section."""
        return pmui.Paper(
            pmui.Typography("📋 Recent Data", variant="h6", styles={"marginBottom": "15px"}),
            # Table will be added reactively
            self.data_table,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_layout(self):
        """Create the main dashboard layout."""
        self._layout = pmui.Container(
            self._header,
            self._kpi_section,
            self._chart_section,
            self._table_section,
            width_option="xl"
        )
    
    @property
    def filtered_data(self):
        """Get filtered data based on selected time range."""
        end_date = self.data['timestamp'].max()
        # Get parameter value safely
        days = getattr(self, 'days', 7)
        if not isinstance(days, (int, float)):
            days = 7
        start_date = end_date - datetime.timedelta(days=int(days))
        return self.data[self.data['timestamp'] >= start_date].copy()
    
    @param.depends("metric", "frequency", "aggregation", "days", "color")
    def time_series_plot(self):
        """Generate interactive time series plot."""
        # Get filtered data
        data = self.filtered_data
        
        if len(data) == 0:
            return pmui.Alert(
                object="No data available for the selected time range",
                alert_type="warning"
            )
        
        # Get parameter values safely
        metric = getattr(self, 'metric', 'temperature_c')
        frequency = getattr(self, 'frequency', 'H')
        aggregation = getattr(self, 'aggregation', 'mean')
        color = getattr(self, 'color', '#1976d2')
        
        # Ensure string values
        metric = str(metric) if metric is not None else 'temperature_c'
        frequency = str(frequency) if frequency is not None else 'H'
        aggregation = str(aggregation) if aggregation is not None else 'mean'
        color = str(color) if color is not None else '#1976d2'
        
        # Resample data if needed
        if frequency != 'H':
            resampled = data.set_index('timestamp').resample(frequency)
            if aggregation == 'mean':
                data = resampled.mean().reset_index()
            elif aggregation == 'median':
                data = resampled.median().reset_index()
            elif aggregation == 'min':
                data = resampled.min().reset_index()
            elif aggregation == 'max':
                data = resampled.max().reset_index()
            elif aggregation == 'std':
                data = resampled.std().reset_index()
        
        # Create plot
        unit = self._get_unit_for_metric(metric)
        title = f"{metric.replace('_', ' ').title()} ({unit})"
        
        plot = data.hvplot(
            x='timestamp',
            y=metric,
            kind='line',
            color=color,
            title=title,
            xlabel='Time',
            ylabel=unit,
            responsive=True,
            min_height=300
        )
        
        # Convert to Panel pane and wrap in Material UI Paper
        pane = pn.pane.HoloViews(plot, sizing_mode="stretch_width")
        return pmui.Paper(pane, sizing_mode="stretch_width")
    
    @param.depends("days")
    def data_table(self):
        """Display recent data in a table."""
        data = self.filtered_data.tail(10)  # Show last 10 records
        
        if len(data) == 0:
            return pmui.Alert(
                object="No data available for the selected time range",
                alert_type="warning"
            )
        
        # Format timestamp
        data = data.copy()
        data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Create table
        table = pn.widgets.Tabulator(
            data,
            pagination='local',
            page_size=10,
            sizing_mode="stretch_width"
        )
        
        return table
    
    def _get_unit_for_metric(self, metric):
        """Get unit for a given metric."""
        units = {
            'temperature_c': '°C',
            'humidity_pct': '%',
            'pressure_hpa': 'hPa',
            'co2_ppm': 'ppm',
            'light_lux': 'lux',
            'sound_db': 'dB'
        }
        return units.get(metric, '')
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """
        Create a servable dashboard app following Panel best practices.
        
        Demonstrates proper use of Material UI Page with sidebar controls
        and main content area.
        """
        instance = cls(**params)
        
        # Create Page with Siemens iX theme
        page = pmui.Page(
            title="Environmental Analytics Dashboard - Siemens iX",
            main=[instance],
            sidebar=[instance._control_widgets],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension('tabulator', 'plotly', 'vega', notifications=True)

# Apply Siemens iX configuration
configure()


# Serve the app
if __name__ == "__main__":
    # Run with `python time_series_dashboard.py`
    TimeSeriesDashboard.create_app().show(port=5007, autoreload=True, open=True)
elif pn.state.served:
    # Run with `panel serve time_series_dashboard.py --port 5007 --dev --show`
    TimeSeriesDashboard.create_app().servable()