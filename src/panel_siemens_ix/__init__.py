"""
Panel Siemens iX - Material-UI theme based on Siemens iX design system
"""
import panel as pn
import panel_material_ui as pmui
from pathlib import Path

# Import theme functionality
from .theme import (
    create_theme,
    siemens_ix_light_theme,
    siemens_ix_dark_theme,
    SiemensIXDarkColors,
)
from .colors import (
    SiemensIXLightColors,
    get_colors,
    get_continuous_cmap,
    get_categorical_palette,
)

__version__ = "0.1.0"

# Custom notification message
_DISCONNECT_NOTIFICATION: str = """The connection to the server was lost. Please refresh to \
reconnect."""

FAVICON_PATH = Path(__file__).parent / "static/sie-favicon_intranet.png"
LOGO_LIGHT_PATH = Path(__file__).parent / "static/sie-logo-black-rgb.svg"
LOGO_DARK_PATH = Path(__file__).parent / "static/sie-logo-white-rgb.svg"

def _configure_session() -> None:
    """
    Configure Panel session-specific settings.

    This includes disconnect notifications and other session-level configurations.
    """
    pn.config.disconnect_notification = _DISCONNECT_NOTIFICATION


@pn.cache
def _configure_general() -> None:
    """
    Configure general theme settings for Panel Material UI components.

    This includes theme configuration, CSS, fonts, logos, and component defaults.
    """
    # Page configuration
    pmui.Page.param.theme_config.default = dict(light=siemens_ix_light_theme, dark=siemens_ix_dark_theme)
    # CSS and font configuration

    # Brand assets configuration
    pmui.Page.param.logo.default = {"light": LOGO_LIGHT_PATH, "dark": LOGO_DARK_PATH}
    pmui.Page.favicon = FAVICON_PATH
    #pmui.Page.meta.apple_touch_icon = ""  # Intentionally left empty
    #pmui.Page.meta.title = "Siemens"

    # Component-specific configurations
    #pmui.Button.param.disable_elevation.default = True



def configure() -> None:
    """
    Configure the complete theme for the application.

    This is the main entry point for applying the Orbitron brand theme
    to a Panel Material UI application.

    Examples
    --------
    >>> from brand.mui import configure
    >>> configure()
    >>> app = pmui.Page(title="My Orbitron App")
    """
    _configure_general()
    _configure_session()


__all__ = [
    "configure",
    "__version__",
    "create_theme",
    "get_colors",
    "siemens_ix_light_theme",
    "siemens_ix_dark_theme",
    "SiemensIXDarkColors",
    "SiemensIXLightColors",
    "get_continuous_cmap",
    "get_categorical_palette",
]
