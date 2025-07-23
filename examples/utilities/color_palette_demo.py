"""
Siemens iX Color Palette Demo

This example demonstrates the comprehensive color system of the Siemens iX
design system, including semantic colors, continuous color maps, and 
categorical palettes. It shows how to use the color utilities provided
by panel-siemens-ix.

Run with:
    panel serve color_palette_demo.py --dev --show
Or:
    python color_palette_demo.py
"""

import panel as pn
import panel_material_ui as pmui
import param
from panel_siemens_ix import configure
from panel_siemens_ix.colors import (
    get_colors, 
    get_continuous_cmap, 
    get_categorical_palette,
    SiemensIXLightColors,
    SiemensIXDarkColors,
    _hex_to_rgba
)
import numpy as np


class ColorPaletteDemo(pn.viewable.Viewer):
    """
    Interactive demonstration of the Siemens iX color system.
    
    This class showcases all available colors, their usage, and utility functions
    for generating color palettes and themes.
    """
    
    # Parameters for interactive exploration
    current_theme = param.Selector(
        default="light",
        objects=["light", "dark"],
        doc="Current theme mode"
    )
    palette_size = param.Integer(
        default=8, bounds=(3, 20),
        doc="Number of colors in categorical palette"
    )
    alpha_value = param.Number(
        default=1.0, bounds=(0.1, 1.0),
        doc="Alpha transparency for color demonstrations"
    )
    
    def __init__(self, **params):
        super().__init__(**params)
        
        # DO use sizing_mode="stretch_width" for components by default
        with pn.config.set(sizing_mode="stretch_width"):
            self._create_sections()
            self._create_layout()
    
    def _create_sections(self):
        """Create different color demonstration sections."""
        self._semantic_colors_section = self._create_semantic_colors_section()
        self._component_colors_section = self._create_component_colors_section()
        self._utility_functions_section = self._create_utility_functions_section()
        self._palette_generation_section = self._create_palette_generation_section()
        self._usage_examples_section = self._create_usage_examples_section()
    
    def _create_semantic_colors_section(self):
        """Create semantic colors demonstration."""
        
        def create_color_card(color_name, color_dict, description):
            """Create a card showing color variants."""
            color_chips = []
            for variant, hex_color in color_dict.items():
                color_chips.append(
                    pmui.Paper(
                        pmui.Typography(variant.title(), variant="caption"),
                        pmui.Typography(hex_color, variant="body2", styles={"fontFamily": "monospace"}),
                        styles={
                        "padding": "8px",
                        "margin": "4px",
                        "backgroundColor": hex_color,
                        "color": color_dict.get('contrast', '#000000'),
                        "minHeight": "60px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center"
                    })
                )
            
            return pmui.Card(
                pmui.Typography(color_name, variant="h6", styles={"marginBottom": "10px"}),
                pmui.Typography(description, variant="body2", styles={"marginBottom": "15px"}),
                pmui.Row(*color_chips, styles={"flexWrap": "wrap"}),
                styles={"padding": "15px", "margin": "10px"})
        
        semantic_colors_display = pmui.Column(
            pmui.Typography(object=self.semantic_colors_title, variant="body1"),
            pmui.Row(
                pmui.Column(
                    self.primary_color_card,
                    self.secondary_color_card,
                    self.success_color_card
                ),
                pmui.Column(
                    self.warning_color_card,
                    self.error_color_card,
                    self.info_color_card
                )
            )
        )
        
        return pmui.Card(
            pmui.Typography("Semantic Colors", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "Semantic colors provide consistent meaning across the interface:",
                variant="body2",
                styles={"marginBottom": "20px"}
            ),
            semantic_colors_display,
            styles={"padding": "20px", "marginBottom": "20px"})
    
    def _create_component_colors_section(self):
        """Create component-specific colors demonstration."""
        
        component_colors_display = pmui.Column(
            pmui.Typography(object=self.component_colors_info, variant="body1"),
            pmui.Row(
                pmui.Column(
                    self.text_colors_card,
                    self.background_colors_card
                ),
                pmui.Column(
                    self.border_colors_card,
                    self.ghost_colors_card
                )
            )
        )
        
        return pmui.Card(
            pmui.Typography("Component Colors", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "Colors specifically designed for UI components and interfaces:",
                variant="body2",
                styles={"marginBottom": "20px"}
            ),
            component_colors_display,
            styles={"padding": "20px", "marginBottom": "20px"})
    
    def _create_utility_functions_section(self):
        """Create utility functions demonstration."""
        
        # Alpha transparency demonstration
        alpha_demo = pmui.Column(
            pmui.Typography("Alpha Transparency:", variant="subtitle2"),
            pmui.Typography(object=self.alpha_demo_display, variant="body2"),
            pmui.FloatSlider.from_param(
                self.param.alpha_value,
                name="Alpha Value",
                styles={"margin": "10px 0"}
            )
        )
        
        # Color conversion examples
        conversion_demo = pmui.Column(
            pmui.Typography("Color Conversion Examples:", variant="subtitle2"),
            pmui.Typography(object=self.conversion_examples, variant="body2", styles={"fontFamily": "monospace"})
        )
        
        return pmui.Card(
            pmui.Typography("Utility Functions", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "Helper functions for working with colors:",
                variant="body2",
                styles={"marginBottom": "20px"}
            ),
            alpha_demo,
            pmui.Divider(styles={"margin": "20px 0"}),
            conversion_demo,
            styles={"padding": "20px", "marginBottom": "20px"})
    
    def _create_palette_generation_section(self):
        """Create palette generation demonstration."""
        
        continuous_palette_display = pmui.Column(
            pmui.Typography("Continuous Color Map:", variant="subtitle2"),
            pmui.Typography(object=self.continuous_palette_info, variant="body2"),
            self.continuous_palette_visual
        )
        
        categorical_palette_display = pmui.Column(
            pmui.Typography("Categorical Palette:", variant="subtitle2"),
            pmui.IntSlider.from_param(
                self.param.palette_size,
                name="Palette Size",
                styles={"margin": "10px 0"}
            ),
            self.categorical_palette_visual
        )
        
        return pmui.Card(
            pmui.Typography("Palette Generation", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "Generate color palettes for data visualization:",
                variant="body2",
                styles={"marginBottom": "20px"}
            ),
            continuous_palette_display,
            pmui.Divider(styles={"margin": "20px 0"}),
            categorical_palette_display,
            styles={"padding": "20px", "marginBottom": "20px"})
    
    def _create_usage_examples_section(self):
        """Create practical usage examples."""
        
        code_examples = pmui.Column(
            pmui.Typography("Code Examples:", variant="subtitle2"),
            pmui.Paper(
                pmui.Typography(object=self.code_examples_display, variant="body2", styles={"fontFamily": "monospace"}),
                styles={"padding": "15px", "backgroundColor": "grey.100"}
            )
        )
        
        return pmui.Card(
            pmui.Typography("Usage Examples", variant="h6", styles={"marginBottom": "15px"}),
            pmui.Typography(
                "How to use Siemens iX colors in your applications:",
                variant="body2",
                styles={"marginBottom": "20px"}
            ),
            code_examples,
            styles={"padding": "20px", "marginBottom": "20px"})
    
    def _create_layout(self):
        """Create the main application layout."""
        
        # Header with theme selector
        header = pmui.Paper(
            pmui.Row(
                pmui.Column(
                    pmui.Typography("🎨 Siemens iX Color System", variant="h4"),
                    pmui.Typography(
                        "Comprehensive demonstration of the Siemens iX color palette and utilities",
                        variant="body1"
                    )
                ),
                pmui.Select.from_param(
                    self.param.current_theme,
                    name="Theme Mode",
                    styles={"minWidth": "150px"}
                ),
                styles={"justifyContent": "space-between", "alignItems": "center"}
            ),
            styles={"padding": "30px", "marginBottom": "20px"}
        )
        
        # Main content
        self._layout = pmui.Container(
            header,
            self._semantic_colors_section,
            self._component_colors_section,
            self._utility_functions_section,
            self._palette_generation_section,
            self._usage_examples_section,
            width_option="xl"
        )
    
    # Reactive methods for color displays
    
    @param.depends("current_theme")
    def semantic_colors_title(self):
        """Display current theme information."""
        colors = get_colors(self.current_theme)
        return f"Current theme: {self.current_theme.title()} | Color class: {type(colors).__name__}"
    
    @param.depends("current_theme")
    def primary_color_card(self):
        """Create primary color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Primary", colors.primary, "Main brand color for buttons, links, and highlights")
    
    @param.depends("current_theme")
    def secondary_color_card(self):
        """Create secondary color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Secondary", colors.secondary, "Supporting color for secondary actions")
    
    @param.depends("current_theme")
    def success_color_card(self):
        """Create success color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Success", colors.success, "Positive states and successful actions")
    
    @param.depends("current_theme")
    def warning_color_card(self):
        """Create warning color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Warning", colors.warning, "Caution states and important notices")
    
    @param.depends("current_theme")
    def error_color_card(self):
        """Create error color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Error", colors.error, "Error states and destructive actions")
    
    @param.depends("current_theme")
    def info_color_card(self):
        """Create info color card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Info", colors.info, "Informational messages and hints")
    
    def _create_color_card_content(self, name, color_dict, description):
        """Helper to create color card content."""
        color_swatches = []
        for variant, hex_color in color_dict.items():
            color_swatches.append(
                pmui.Paper(
                    pmui.Typography(variant, variant="caption", styles={"fontWeight": "bold"}),
                    pmui.Typography(hex_color, variant="body2", styles={"fontFamily": "monospace", "fontSize": "12px"}),
                    styles={
                    "padding": "8px",
                    "margin": "2px",
                    "backgroundColor": hex_color,
                    "color": color_dict.get('contrast', '#ffffff'),
                    "minHeight": "50px",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "borderRadius": "4px"
                })
            )
        
        return pmui.Card(
            pmui.Typography(name, variant="subtitle1", styles={"marginBottom": "8px"}),
            pmui.Typography(description, variant="caption", styles={"marginBottom": "12px", "color": "text.secondary"}),
            pmui.Row(*color_swatches, styles={"flexWrap": "wrap"}),
            styles={"padding": "12px", "margin": "8px"})
    
    @param.depends("current_theme")
    def component_colors_info(self):
        """Display component colors information."""
        return f"Component colors for {self.current_theme} theme:"
    
    @param.depends("current_theme")
    def text_colors_card(self):
        """Create text colors card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Text", colors.text, "Text colors for different hierarchy levels")
    
    @param.depends("current_theme")
    def background_colors_card(self):
        """Create background colors card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Background", colors.background, "Background colors for surfaces and containers")
    
    @param.depends("current_theme")
    def border_colors_card(self):
        """Create border colors card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Border", colors.border, "Border colors for dividers and outlines")
    
    @param.depends("current_theme")
    def ghost_colors_card(self):
        """Create ghost colors card."""
        colors = get_colors(self.current_theme)
        return self._create_color_card_content("Ghost", colors.ghost, "Transparent states and subtle interactions")
    
    @param.depends("current_theme", "alpha_value")
    def alpha_demo_display(self):
        """Demonstrate alpha transparency."""
        colors = get_colors(self.current_theme)
        primary_color = colors.primary["main"]
        rgba_color = _hex_to_rgba(primary_color, self.alpha_value)
        return f"Primary color: {primary_color} → With alpha {self.alpha_value}: {rgba_color}"
    
    @param.depends("current_theme")
    def conversion_examples(self):
        """Show color conversion examples."""
        colors = get_colors(self.current_theme)
        examples = [
            f"# Get colors for current theme",
            f"colors = get_colors('{self.current_theme}')",
            f"",
            f"# Access semantic colors",
            f"primary = colors.primary['main']  # {colors.primary['main']}",
            f"primary_hover = colors.primary['hover']  # {colors.primary['hover']}",
            f"",
            f"# Convert to RGBA with transparency",
            f"transparent = _hex_to_rgba(primary, 0.5)",
            f"# Result: {_hex_to_rgba(colors.primary['main'], 0.5)}"
        ]
        return "\n".join(examples)
    
    @param.depends("current_theme")
    def continuous_palette_info(self):
        """Show continuous palette information."""
        return f"Continuous color map for {self.current_theme} theme (256 colors from white/dark to primary)"
    
    @param.depends("current_theme")
    def continuous_palette_visual(self):
        """Create continuous palette visualization."""
        cmap = get_continuous_cmap(self.current_theme == "dark")
        
        # Create color bars
        color_bars = []
        for i, color in enumerate(cmap[::32]):  # Show every 32nd color
            color_bars.append(
                pmui.Paper("", styles={
                    "backgroundColor": color,
                    "width": "20px",
                    "height": "30px",
                    "margin": "1px",
                    "display": "inline-block"
                })
            )
        
        return pmui.Row(*color_bars)
    
    @param.depends("current_theme", "palette_size")
    def categorical_palette_visual(self):
        """Create categorical palette visualization."""
        palette = get_categorical_palette(self.current_theme == "dark", self.palette_size)
        
        # Create color swatches with labels
        color_swatches = []
        for i, color in enumerate(palette):
            color_swatches.append(
                pmui.Paper(
                    pmui.Typography(f"{i+1}", variant="caption", styles={"fontWeight": "bold"}),
                    pmui.Typography(color, variant="body2", styles={"fontFamily": "monospace", "fontSize": "11px"}),
                    styles={
                    "backgroundColor": color,
                    "color": "#ffffff",
                    "padding": "8px",
                    "margin": "4px",
                    "minHeight": "60px",
                    "minWidth": "80px",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "textAlign": "center",
                    "borderRadius": "4px"
                })
            )
        
        return pmui.Row(*color_swatches, styles={"flexWrap": "wrap"})
    
    @param.depends("current_theme", "palette_size")
    def code_examples_display(self):
        """Show practical code examples."""
        examples = [
            f"# Import color utilities",
            f"from panel_siemens_ix.colors import get_colors, get_continuous_cmap, get_categorical_palette",
            f"",
            f"# Get current theme colors",
            f"colors = get_colors('{self.current_theme}')",
            f"",
            f"# Use in Material UI components",
            f"button = pmui.Button(",
            f"    name='Primary Action',",
            f"    styles={{'backgroundColor': colors.primary['main']}}",
            f")",
            f"",
            f"# Generate palettes for visualization",
            f"categorical = get_categorical_palette(dark_theme={self.current_theme == 'dark'}, n_colors={self.palette_size})",
            f"continuous = get_continuous_cmap(dark_theme={self.current_theme == 'dark'})",
            f"",
            f"# Use with plotting libraries",
            f"# df.hvplot.scatter(color=categorical[0], cmap=continuous)"
        ]
        return "\n".join(examples)
    
    def __panel__(self):
        """Method for displaying the component in notebook settings."""
        return self._layout
    
    @classmethod
    def create_app(cls, **params):
        """Create a servable color palette demo application."""
        instance = cls(**params)
        
        # Sidebar with color information
        sidebar_content = pmui.Column(
            pmui.Typography("Color System Info", variant="h6"),
            pmui.Typography(
                "The Siemens iX color system provides:",
                variant="body2",
                styles={"marginBottom": "15px"}
            ),
            pmui.Alert(
                object="🎯 Semantic colors for consistent meaning",
                alert_type="info",
                styles={"marginBottom": "10px"}
            ),
            pmui.Alert(
                object="🎨 Component-specific color variations",
                alert_type="success",
                styles={"marginBottom": "10px"}
            ),
            pmui.Alert(
                object="📊 Palette generation for data visualization",
                alert_type="warning",
                styles={"marginBottom": "10px"}
            ),
            pmui.Alert(
                object="♿ WCAG compliant contrast ratios",
                alert_type="error",
                styles={"marginBottom": "20px"}
            ),
            pmui.Typography("Color Classes:", variant="subtitle2"),
            pmui.Typography("• SiemensIXLightColors", variant="body2"),
            pmui.Typography("• SiemensIXDarkColors", variant="body2"),
            pmui.Typography("", variant="body2"),  # Spacer
            pmui.Typography("Utility Functions:", variant="subtitle2"),
            pmui.Typography("• get_colors(mode)", variant="body2"),
            pmui.Typography("• get_continuous_cmap()", variant="body2"),
            pmui.Typography("• get_categorical_palette()", variant="body2"),
            pmui.Typography("• _hex_to_rgba()", variant="body2"),
        )
        
        page = pmui.Page(
            title="Color System - Siemens iX",
            main=[instance],
            sidebar=[sidebar_content],
            theme_toggle=True
        )
        
        return page


# Enable Panel extensions
pn.extension()

# Apply Siemens iX configuration
configure()


# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python color_palette_demo.py`
    ColorPaletteDemo.create_app().show(port=5007, autoreload=True, open=True)

# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve color_palette_demo.py --port 5007 --dev --show`
    ColorPaletteDemo.create_app().servable()