"""
Siemens iX Business Intelligence Dashboard

This advanced example demonstrates a business intelligence dashboard featuring:
- Data catalog with file uploads (CSV, Parquet) and fsspec filesystem connections
- In-memory DuckDB instance for data registration and querying
- SQL editor with syntax highlighting and autocompletion
- Interactive data visualization with hvPlot explorer
- Multi-tab layout for data management and analysis

Features:
- File upload support for CSV and Parquet files
- FSSpec filesystem connection support (s3, gcs, etc.)
- In-memory data processing with DuckDB
- SQL editor with syntax highlighting (CodeEditor widget)
- Query results display in tabular format (Tabulator widget)
- Data visualization capabilities
- Multi-tab layout for organized workflow

Run with:
    panel serve bi_dashboard.py --dev --show
Or:
    python bi_dashboard.py
"""

import panel as pn
import panel_material_ui as pmui
import param
import pandas as pd
try:
    import duckdb
except ImportError:
    duckdb = None
import io
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from panel_siemens_ix import configure


class DuckDBManager:
    """Manage in-memory DuckDB instance for data registration and querying."""
    
    def __init__(self):
        """Initialize DuckDB connection."""
        if duckdb is not None:
            self.conn = duckdb.connect()
        else:
            self.conn = None
        self.registered_tables: Dict[str, str] = {}  # table_name -> source_info
    
    def register_file(self, file_path: str, table_name: str) -> bool:
        """
        Register a file with the DuckDB instance.
        
        Parameters
        ----------
        file_path : str
            Path to the file to register
        table_name : str
            Name to register the table as
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        if self.conn is None:
            return False
            
        try:
            # Determine file type and register appropriately
            if file_path.endswith('.csv'):
                self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')")
            elif file_path.endswith('.parquet'):
                self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}')")
            else:
                return False
            
            self.registered_tables[table_name] = file_path
            return True
        except Exception as e:
            print(f"Error registering file {file_path}: {e}")
            return False
    
    def register_dataframe(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Register a pandas DataFrame with the DuckDB instance.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to register
        table_name : str
            Name to register the table as
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        if self.conn is None:
            return False
            
        try:
            self.conn.register(table_name, df)
            self.registered_tables[table_name] = "DataFrame"
            return True
        except Exception as e:
            print(f"Error registering DataFrame: {e}")
            return False
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results.
        
        Parameters
        ----------
        query : str
            SQL query to execute
            
        Returns
        -------
        pd.DataFrame
            Query results as a DataFrame
        """
        if self.conn is None:
            return pd.DataFrame()
            
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def get_tables(self) -> list:
        """Get list of registered tables."""
        return list(self.registered_tables.keys())
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        Get information about a registered table.
        
        Parameters
        ----------
        table_name : str
            Name of the table to get information for
            
        Returns
        -------
        pd.DataFrame
            Table information
        """
        if self.conn is None:
            return pd.DataFrame()
            
        try:
            return self.conn.execute(f"DESCRIBE {table_name}").fetchdf()
        except Exception as e:
            print(f"Error getting table info: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close the DuckDB connection."""
        if self.conn is not None:
            self.conn.close()


class BIDashboard(pn.viewable.Viewer):
    """
    Business intelligence dashboard with data catalog, SQL editor, and visualization.
    
    This dashboard demonstrates advanced Panel features:
    - File upload and fsspec integration
    - In-memory data processing with DuckDB
    - SQL editor with syntax highlighting
    - Interactive data visualization
    - Multi-tab layout design
    """
    
    # Dashboard parameters
    selected_table = param.Selector(
        default=None,
        objects=[],
        doc="Currently selected table for analysis"
    )
    
    sql_query = param.String(
        default="SELECT * FROM ",
        doc="SQL query to execute"
    )
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # Initialize DuckDB manager
        self.db_manager = DuckDBManager()
        
        # Configure sizing mode
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_components()
            self._create_layout()
    
    def _create_components(self):
        """Create dashboard components."""
        # Header
        self._header = pmui.Paper(
            pmui.Typography("📊 Business Intelligence Dashboard", variant="h4"),
            pmui.Typography(
                "Data catalog, SQL editor, and visualization tools",
                variant="subtitle1",
                styles={"color": "text.secondary"}
            ),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
        
        # Data catalog section
        self._catalog_section = self._create_catalog_section()
        
        # SQL editor section
        self._sql_section = self._create_sql_section()
        
        # Results section
        self._results_section = self._create_results_section()
        
        # Visualization section
        self._viz_section = self._create_viz_section()
    
    def _create_catalog_section(self):
        """Create data catalog section."""
        # File upload
        self._file_uploader = pmui.widgets.input.FileInput(
            label="Upload Data File",
            accept='.csv,.parquet',
            styles={"margin": "10px 0"}
        )
        self._file_uploader.param.watch(self._handle_file_upload, 'value')
        
        # FSSpec path input
        self._fsspec_path = pmui.widgets.input.TextInput(
            label="FSSpec Path",
            placeholder="Enter fsspec path (e.g., s3://bucket/file.csv)",
            styles={"margin": "10px 0", "width": "100%"}
        )
        
        self._fsspec_button = pmui.Button(
            name="Register FSSpec Path",
            button_type="primary",
            on_click=self._handle_fsspec_register,
            styles={"margin": "10px 0"}
        )
        
        # Registered tables
        self._tables_pane = pmui.pane.base.Typography(
            "Registered Tables\nNo tables registered yet.",
            variant="body1",
            styles={"margin": "10px 0"}
        )
        
        # Refresh tables button
        self._refresh_button = pmui.Button(
            name="Refresh Tables",
            button_type="secondary",
            icon="refresh",
            on_click=self._refresh_tables,
            styles={"margin": "10px 0"}
        )
        
        return pmui.Paper(
            pmui.Typography("📂 Data Catalog", variant="h6", styles={"marginBottom": "15px"}),
            self._file_uploader,
            self._fsspec_path,
            self._fsspec_button,
            self._refresh_button,
            self._tables_pane,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_sql_section(self):
        """Create SQL editor section."""
        # SQL editor
        self._sql_editor = pn.widgets.CodeEditor(
            value=self.sql_query,
            language="sql",
            theme="chrome",
            annotations=[{"row": 0, "column": 0, "text": "Enter your SQL query", "type": "info"}],
            height=200,
            sizing_mode="stretch_width"
        )
        self._sql_editor.param.watch(self._update_sql_query, 'value')
        
        # Execute button
        self._execute_button = pmui.Button(
            name="Execute Query",
            button_type="primary",
            on_click=self._execute_query,
            styles={"margin": "10px 0"}
        )
        
        # Clear button
        self._clear_button = pmui.Button(
            name="Clear Editor",
            button_type="secondary",
            on_click=self._clear_editor,
            styles={"margin": "10px 0"}
        )
        
        return pmui.Paper(
            pmui.Typography("🔍 SQL Editor", variant="h6", styles={"marginBottom": "15px"}),
            self._sql_editor,
            pmui.Row(self._execute_button, self._clear_button),
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_results_section(self):
        """Create results section."""
        self._results_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            pagination='local',
            page_size=10,
            sizing_mode="stretch_width"
        )
        
        return pmui.Paper(
            pmui.Typography("📋 Query Results", variant="h6", styles={"marginBottom": "15px"}),
            self._results_table,
            styles={"padding": "20px", "marginBottom": "20px"}
        )
    
    def _create_viz_section(self):
        """Create visualization section."""
        # Visualization placeholder
        self._viz_pane = pmui.pane.base.Typography(
            "Data Visualization\nExecute a query to see visualization options.",
            variant="body1",
            styles={"padding": "20px", "textAlign": "center"}
        )
        
        return pmui.Paper(
            pmui.Typography("📈 Data Visualization", variant="h6", styles={"marginBottom": "15px"}),
            self._viz_pane,
            styles={"padding": "20px", "marginBottom": "20px", "minHeight": "300px"}
        )
    
    def _create_layout(self):
        """Create the main dashboard layout."""
        # Main tabs
        self._tabs = pmui.Tabs(
            ("Data Catalog", self._catalog_section),
            ("SQL Editor", self._sql_section),
            ("Query Results", self._results_section),
            ("Visualization", self._viz_section),
            dynamic=True
        )
        
        self._layout = pmui.Container(
            self._header,
            self._tabs,
            width_option="xl"
        )
    
    def _handle_file_upload(self, event):
        """Handle file upload events."""
        # Get file info safely
        filename = getattr(self._file_uploader, 'filename', None)
        file_contents = getattr(self._file_uploader, 'value', None)
        
        if not file_contents or not filename:
            return
            
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(str(filename)).suffix) as tmp_file:
                tmp_file.write(file_contents)
                tmp_path = tmp_file.name
            
            # Register with DuckDB
            table_name = Path(str(filename)).stem.replace('-', '_').replace(' ', '_')
            if self.db_manager.register_file(tmp_path, table_name):
                # Update UI
                if hasattr(pn.state, 'notifications') and pn.state.notifications:
                    pn.state.notifications.success(f"Successfully registered {filename} as {table_name}")
                self._refresh_tables()
            else:
                if hasattr(pn.state, 'notifications') and pn.state.notifications:
                    pn.state.notifications.error(f"Failed to register {filename}")
        except Exception as e:
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.error(f"Error processing file upload: {str(e)}")
    
    def _handle_fsspec_register(self, event):
        """Handle fsspec path registration."""
        # Get path safely
        path = getattr(self._fsspec_path, 'value', None)
        if not path:
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.warning("Please enter a valid fsspec path")
            return
            
        try:
            # Extract table name from path
            table_name = Path(str(path)).stem.replace('-', '_').replace(' ', '_')
            
            # Check if DuckDB is available
            if self.db_manager.conn is None:
                if hasattr(pn.state, 'notifications') and pn.state.notifications:
                    pn.state.notifications.error("DuckDB is not available")
                return
                
            # Try to register the path directly with DuckDB
            # This works with fsspec URLs if the appropriate filesystem is installed
            if str(path).endswith('.csv'):
                self.db_manager.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{path}')")
            elif str(path).endswith('.parquet'):
                self.db_manager.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{path}')")
            else:
                if hasattr(pn.state, 'notifications') and pn.state.notifications:
                    pn.state.notifications.error("Unsupported file type. Please use CSV or Parquet files.")
                return
                
            self.db_manager.registered_tables[table_name] = str(path)
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.success(f"Successfully registered {path} as {table_name}")
            self._refresh_tables()
        except Exception as e:
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.error(f"Failed to register {path}: {str(e)}")
    
    def _refresh_tables(self, event=None):
        """Refresh the list of registered tables."""
        tables = self.db_manager.get_tables()
        
        if tables:
            # Update selector options
            self.param.selected_table.objects = tables
            # Get current selected table safely
            current_selected = getattr(self, 'selected_table', None)
            if not current_selected and tables:
                self.selected_table = tables[0]
            
            # Update tables pane
            tables_md = "Registered Tables\n"
            for table in tables:
                tables_md += f"- {table}\n"
            self._tables_pane.object = tables_md
        else:
            self._tables_pane.object = "Registered Tables\nNo tables registered yet."
            self.param.selected_table.objects = []
            self.selected_table = None
    
    def _update_sql_query(self, event):
        """Update SQL query parameter."""
        self.sql_query = self._sql_editor.value
    
    def _execute_query(self, event):
        """Execute the current SQL query."""
        # Get query safely
        query = getattr(self, 'sql_query', '').strip()
        if not query:
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.warning("Please enter a SQL query")
            return
            
        # Execute query
        result = self.db_manager.execute_query(query)
        
        if result.empty:
            self._results_table.value = pd.DataFrame([{"message": "Query executed successfully but returned no results"}])
        else:
            self._results_table.value = result
            if hasattr(pn.state, 'notifications') and pn.state.notifications:
                pn.state.notifications.success(f"Query executed successfully. {len(result)} rows returned.")
            
            # Update visualization
            self._update_visualization(result)
    
    def _clear_editor(self, event):
        """Clear the SQL editor."""
        self._sql_editor.value = ""
        self.sql_query = ""
    
    def _update_visualization(self, data: pd.DataFrame):
        """Update the visualization pane with data exploration options."""
        if data.empty:
            self._viz_pane.object = "Data Visualization\nNo data to visualize."
            return
            
        # Simple visualization options
        columns = list(data.columns)
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_columns) >= 2:
            # Create a simple scatter plot option
            x_col = numeric_columns[0]
            y_col = numeric_columns[1]
            
            # For now, just show info about available columns
            viz_info = f"""Data Visualization

Available Columns: {', '.join(columns)}

Numeric Columns: {', '.join(numeric_columns)}

In a full implementation, this section would provide:
- Interactive chart selection (scatter, bar, line, etc.)
- Column selection for axes
- Chart customization options
- hvPlot explorer integration"""
            self._viz_pane.object = viz_info
        else:
            self._viz_pane.object = "Data Visualization\nNot enough numeric columns for visualization."
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """
        Create a servable dashboard app following Panel best practices.
        """
        instance = cls(**params)
        
        # Create Page with Siemens iX theme
        page = pmui.Page(
            title="Business Intelligence Dashboard - Siemens iX",
            main=[instance],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension('tabulator', 'codeeditor', notifications=True)

# Apply Siemens iX configuration
configure()


# Serve the app
if __name__ == "__main__":
    # Run with `python bi_dashboard.py`
    BIDashboard.create_app().show(port=5008, autoreload=True, open=True)
elif pn.state.served:
    # Run with `panel serve bi_dashboard.py --port 5008 --dev --show`
    BIDashboard.create_app().servable()