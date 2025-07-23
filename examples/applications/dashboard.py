"""
Siemens iX Dashboard Application

This example demonstrates a complete dashboard application following Panel best practices:
- Parameter-driven architecture with pn.viewable.Viewer
- Static layout with reactive content
- Proper caching for performance
- Material UI components with Siemens iX theming
- Realistic data visualization and KPI tracking

Run with:
    panel serve dashboard.py --dev --show
Or:
    python dashboard.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import pandas as pd
import numpy as np
import datetime
from panel_siemens_ix import configure
from typing import Dict, Any


# DO organize functions to extract data separately as your app grows
@pn.cache(max_items=3, ttl=300)  # Cache for 5 minutes
def extract_sample_data(days: int = 30) -> pd.DataFrame:
    """
    Extract sample industrial data for the dashboard.
    
    In a real application, this would connect to your data sources.
    Uses caching to improve performance for expensive data operations.
    """
    dates = pd.date_range(end=datetime.date.today(), periods=days, freq='D')
    
    # Simulate industrial metrics
    np.random.seed(42)  # For consistent demo data
    data = {
        'date': dates,
        'production_volume': np.random.normal(1000, 100, days).cumsum(),
        'efficiency': np.random.normal(85, 5, days).clip(70, 95),
        'energy_consumption': np.random.normal(500, 50, days),
        'defect_rate': np.random.normal(2.5, 0.5, days).clip(0.5, 5.0),
        'temperature': np.random.normal(22, 3, days),
        'pressure': np.random.normal(1013, 20, days)
    }
    
    return pd.DataFrame(data)


# DO organize functions to transform data separately
@pn.cache(max_items=5)
def transform_kpi_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Transform raw data into KPI metrics.
    
    Uses caching for expensive transformations that return the same
    result for the same input data.
    """
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest
    
    return {
        'production': {
            'current': latest['production_volume'],
            'change': latest['production_volume'] - previous['production_volume'],
            'trend': 'up' if latest['production_volume'] > previous['production_volume'] else 'down'
        },
        'efficiency': {
            'current': latest['efficiency'],
            'change': latest['efficiency'] - previous['efficiency'],
            'trend': 'up' if latest['efficiency'] > previous['efficiency'] else 'down'
        },
        'energy': {
            'current': latest['energy_consumption'],
            'change': latest['energy_consumption'] - previous['energy_consumption'],
            'trend': 'down' if latest['energy_consumption'] < previous['energy_consumption'] else 'up'
        },
        'quality': {
            'current': latest['defect_rate'],
            'change': latest['defect_rate'] - previous['defect_rate'],
            'trend': 'down' if latest['defect_rate'] < previous['defect_rate'] else 'up'
        }
    }


class IndustrialDashboard(pn.viewable.Viewer):
    """
    Industrial dashboard demonstrating Panel best practices with Siemens iX theming.
    
    This dashboard follows the parameter-driven architecture pattern and demonstrates
    proper reactive design with static layout + dynamic content.
    """
    
    # Dashboard parameters for user control
    time_period = param.Integer(
        default=30, bounds=(7, 90),
        doc="Number of days to display in dashboard"
    )
    refresh_rate = param.Selector(
        default="Manual",
        objects=["Manual", "30s", "1m", "5m"],
        doc="Data refresh interval"
    )
    metric_filter = param.Selector(
        default="All Metrics",
        objects=["All Metrics", "Production", "Quality", "Energy"],
        doc="Filter for displayed metrics"
    )
    
    # State parameters
    last_updated = param.Date(default=datetime.date.today(), doc="Last data update")
    alert_count = param.Integer(default=0, doc="Number of active alerts")
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_components()
            self._create_layout()
    
    def _create_components(self):
        """Create dashboard components with static layout."""
        
        # Header section
        self._header = self._create_header()
        
        # KPI cards section  
        self._kpi_section = self._create_kpi_section()
        
        # Charts section
        self._charts_section = self._create_charts_section()
        
        # Data table section
        self._table_section = self._create_table_section()
        
        # Control widgets for sidebar
        self._control_widgets = self._create_control_widgets()
    
    def _create_header(self):
        """Create dashboard header with status information."""
        return pmui.Paper(
            pmui.Row(
                pmui.Column(
                    pmui.Typography("🏭 Industrial Dashboard", variant="h4"),
                    pmui.Typography(
                        object=self.status_display,
                        variant="body2",
                        styles={"color": "text.secondary"}
                    )
                ),
                pmui.Column(
                    pmui.Chip(
                        object=f"🔔 {self.alert_count} Alerts",
                        color="warning" if self.alert_count > 0 else "success",
                        styles={"margin": "5px"}
                    ),
                    pmui.Button(
                        name="Refresh Data",
                        button_type="primary",
                        icon="refresh",
                        on_click=self._refresh_data,
                        size="small"
                    )
                ),
                styles={"justifyContent": "space-between", "alignItems": "center"}
            ),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_kpi_section(self):
        """Create KPI cards section."""
        
        def create_kpi_card(title, value_func, icon, color="primary"):
            """Helper to create consistent KPI cards."""
            return pmui.Card(
                pmui.Row(
                    pmui.Column(
                        pmui.Typography(title, variant="subtitle2"),
                        pmui.Typography(object=value_func, variant="h6")
                    ),
                    pmui.Avatar(icon, styles={"backgroundColor": f"{color}.main"})
                ),
                styles={"padding": "15px", "margin": "5px", "minHeight": "100px"}
            )
        
        # DO create static components with reactive content
        kpi_cards = pmui.Row(
            create_kpi_card("Production Volume", self.production_kpi, "factory", "primary"),
            create_kpi_card("Efficiency", self.efficiency_kpi, "trending_up", "success"),
            create_kpi_card("Energy Usage", self.energy_kpi, "flash_on", "warning"),
            create_kpi_card("Quality Score", self.quality_kpi, "check_circle", "info"),
            styles={"flexWrap": "wrap"}
        )
        
        return pmui.Container(
            pmui.Typography("Key Performance Indicators", variant="h6", styles={"marginBottom": "15px"}),
            kpi_cards,
            styles={"marginBottom": "20px"}
        )
    
    def _create_charts_section(self):
        """Create charts section with visualizations."""
        
        # Chart components - content updated reactively
        trend_chart = pmui.Paper(
            pmui.Typography("Production Trends", variant="h6", styles={"marginBottom": "15px"}),
            # In a real app, this would be a hvplot or matplotlib chart
            pmui.Typography(object=self.chart_placeholder, variant="body1"),
            styles={"padding": "20px", "margin": "10px", "minHeight": "300px"}
        )
        
        efficiency_chart = pmui.Paper(
            pmui.Typography("System Efficiency", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(object=self.efficiency_chart_placeholder, variant="body1"),
            styles={"padding": "20px", "margin": "10px", "minHeight": "300px"}
        )
        
        return pmui.Container(
            pmui.Typography("Analytics", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Row(trend_chart, efficiency_chart),
            styles={"marginBottom": "20px"}
        )
    
    def _create_table_section(self):
        """Create data table section."""
        return pmui.Paper(
            pmui.Typography("Recent Data", variant="h6", styles={"marginBottom": "15px"}),
            # DO use pn.widgets.Tabulator for tabular data
            pmui.Typography(object=self.table_summary, variant="body1"),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_control_widgets(self):
        """Create control widgets for the sidebar."""
        
        # DO create widgets using .from_param method
        time_period_widget = pmui.IntSlider.from_param(
            self.param.time_period,
            name="Time Period (days)",
            styles={"margin": "10px 0"}
        )
        
        refresh_widget = pmui.Select.from_param(
            self.param.refresh_rate,
            name="Refresh Rate",
            styles={"margin": "10px 0"}
        )
        
        filter_widget = pmui.Select.from_param(
            self.param.metric_filter,
            name="Metric Filter",
            styles={"margin": "10px 0"}
        )
        
        return pmui.Column(
            pmui.Typography("Dashboard Controls", variant="h6"),
            time_period_widget,
            refresh_widget,
            filter_widget,
            pmui.Alert(
                object="💡 Adjust settings to customize your dashboard view",
                alert_type="info",
                styles={"marginTop": "20px"}
            )
        )
    
    def _create_layout(self):
        """Create the main dashboard layout."""
        
        # Main dashboard content
        self._layout = pmui.Container(
            self._header,
            self._kpi_section,
            self._charts_section,
            self._table_section,
            width_option="xl"
        )
    
    # Reactive methods using @param.depends
    
    @param.depends("time_period", "last_updated")
    def status_display(self):
        """Display current dashboard status."""
        return f"Showing {self.time_period} days | Last updated: {self.last_updated}"
    
    @param.depends("time_period")
    def production_kpi(self):
        """Calculate production KPI."""
        data = extract_sample_data(self.time_period)
        kpis = transform_kpi_data(data)
        current = kpis['production']['current']
        change = kpis['production']['change']
        trend_icon = "↗️" if kpis['production']['trend'] == 'up' else "↘️"
        return f"{current:,.0f} units {trend_icon} ({change:+.0f})"
    
    @param.depends("time_period")
    def efficiency_kpi(self):
        """Calculate efficiency KPI."""
        data = extract_sample_data(self.time_period)
        kpis = transform_kpi_data(data)
        current = kpis['efficiency']['current']
        change = kpis['efficiency']['change']
        trend_icon = "↗️" if kpis['efficiency']['trend'] == 'up' else "↘️"
        return f"{current:.1f}% {trend_icon} ({change:+.1f}%)"
    
    @param.depends("time_period")
    def energy_kpi(self):
        """Calculate energy KPI."""
        data = extract_sample_data(self.time_period)
        kpis = transform_kpi_data(data)
        current = kpis['energy']['current']
        change = kpis['energy']['change']
        trend_icon = "↗️" if kpis['energy']['trend'] == 'up' else "↘️"
        return f"{current:.0f} kWh {trend_icon} ({change:+.0f})"
    
    @param.depends("time_period")
    def quality_kpi(self):
        """Calculate quality KPI."""
        data = extract_sample_data(self.time_period)
        kpis = transform_kpi_data(data)
        current = kpis['quality']['current']
        change = kpis['quality']['change']
        trend_icon = "↗️" if kpis['quality']['trend'] == 'up' else "↘️"
        return f"{current:.1f}% defects {trend_icon} ({change:+.1f}%)"
    
    @param.depends("time_period", "metric_filter")
    def chart_placeholder(self):
        """Placeholder for production trend chart."""
        data = extract_sample_data(self.time_period)
        avg_production = data['production_volume'].mean()
        return f"📊 Production trend chart for {self.time_period} days\nAverage: {avg_production:,.0f} units\nFilter: {self.metric_filter}"
    
    @param.depends("time_period", "metric_filter")
    def efficiency_chart_placeholder(self):
        """Placeholder for efficiency chart."""
        data = extract_sample_data(self.time_period)
        avg_efficiency = data['efficiency'].mean()
        return f"📈 Efficiency chart for {self.time_period} days\nAverage: {avg_efficiency:.1f}%\nFilter: {self.metric_filter}"
    
    @param.depends("time_period")
    def table_summary(self):
        """Summary of recent data for table section."""
        data = extract_sample_data(self.time_period)
        latest_date = data['date'].iloc[-1].strftime('%Y-%m-%d')
        row_count = len(data)
        return f"📋 Data table showing {row_count} records\nLatest entry: {latest_date}\n(In a real app, this would be a Tabulator widget)"
    
    def _refresh_data(self, event):
        """Handle data refresh button clicks."""
        self.last_updated = datetime.date.today()
        self.alert_count = np.random.randint(0, 5)
        
        # Show notification
        if hasattr(pn.state, 'notifications'):
            pn.state.notifications.success(
                f"Dashboard data refreshed! {self.alert_count} alerts detected.",
                duration=3000
            )
    
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
        
        # DO use Page template for served apps
        page = pmui.Page(
            title="Industrial Dashboard - Siemens iX",
            main=[instance],
            # DO provide input widgets in the sidebar
            sidebar=[instance._control_widgets],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension(notifications=True)

# Apply Siemens iX configuration
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python dashboard.py`
    IndustrialDashboard.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve dashboard.py --port 5007 --dev --show`
    IndustrialDashboard.create_app().servable()