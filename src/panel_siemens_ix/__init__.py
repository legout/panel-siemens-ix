"""
Panel Siemens iX - Material-UI theme based on Siemens iX design system
"""

def hello() -> str:
    return "Hello from panel-siemens-ix!"

# Import theme functionality
from .theme import (
    create_siemens_ix_theme,
    get_siemens_ix_colors,
    siemens_ix_light_theme,
    siemens_ix_dark_theme,
    SIEMENS_IX_DARK_COLORS,
    SIEMENS_IX_LIGHT_COLORS,
)

__version__ = "0.1.0"

__all__ = [
    "hello",
    "create_siemens_ix_theme",
    "get_siemens_ix_colors",
    "siemens_ix_light_theme",
    "siemens_ix_dark_theme",
    "SIEMENS_IX_DARK_COLORS",
    "SIEMENS_IX_LIGHT_COLORS",
]
