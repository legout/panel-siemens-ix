"""
Siemens iX Theme for panel-material-ui

This module provides a Material-UI compatible theme based on the Siemens iX design system,
supporting both light and dark modes with comprehensive color definitions including
hover and active states.
"""

from typing import Dict, Any
from .colors import SiemensIXDarkColors, SiemensIXLightColors, _hex_to_rgba


def create_theme(mode: str = "light") -> Dict[str, Any]:
    """
    Create a Material-UI compatible theme using Siemens iX design system colors.

    Args:
        mode: Theme mode, either 'light' or 'dark'

    Returns:
        Dictionary containing Material-UI theme configuration

    Raises:
        ValueError: If mode is not 'light' or 'dark'
    """
    if mode not in ["light", "dark"]:
        raise ValueError("Mode must be either 'light' or 'dark'")

    colors = SiemensIXDarkColors() if mode == "dark" else SiemensIXLightColors()
    return {
        "palette": {
            "mode": mode,
            "primary": {
                "main": colors.primary["main"],
                "dark": colors.primary["active"],
                "light": colors.primary["hover"],
                "contrastText": colors.primary["contrast"],
            },
            "secondary": {
                "main": colors.dynamic["main"],  # Use dynamic color for secondary
                "dark": colors.dynamic["active"],
                "light": colors.dynamic["hover"],
                "contrastText": colors.dynamic["contrast"],
            },
            "error": {
                "main": colors.error["main"],
                "dark": colors.error["active"],
                "light": colors.error["hover"],
                "contrastText": colors.error["contrast"],
            },
            "warning": {
                "main": colors.warning["main"],
                "dark": colors.warning["active"],
                "light": colors.warning["hover"],
                "contrastText": colors.warning["contrast"],
            },
            "info": {
                "main": colors.info["main"],
                "dark": colors.info["active"],
                "light": colors.info["hover"],
                "contrastText": colors.info["contrast"],
            },
            "success": {
                "main": colors.success["main"],
                "dark": colors.success["active"],
                "light": colors.success["hover"],
                "contrastText": colors.success["contrast"],
            },
            "text": {
                "primary": colors.text["primary"],
                "secondary": colors.text["secondary"],
                "disabled": colors.text["disabled"],
                "hint": colors.text["hint"],
            },
            "background": {
                "default": colors.background["default"],
                "paper": colors.background["paper"],
            },
            "divider": colors.border["std"],
        },
        "components": {
            "MuiButton": {
                "styleOverrides": {
                    "root": {
                        "textTransform": "none",  # Siemens iX uses sentence case
                        "borderRadius": "2px",
                        "fontWeight": 700,
                    },
                    "containedPrimary": {
                        "&:hover": {
                            "backgroundColor": colors.primary["hover"],
                        },
                        "&:active": {
                            "backgroundColor": colors.primary["active"],
                        },
                    },
                    "containedSecondary": {
                        "backgroundColor": colors.dynamic["main"],
                        "color": colors.dynamic["contrast"],
                        "&:hover": {
                            "backgroundColor": colors.dynamic["hover"],
                        },
                        "&:active": {
                            "backgroundColor": colors.dynamic["active"],
                        },
                    },
                    "outlined": {
                        "borderColor": colors.border["std"],
                        "&:hover": {
                            "borderColor": colors.dynamic["main"],
                            "backgroundColor": _hex_to_rgba(
                                colors.dynamic["main"], 0.08
                            ),
                        },
                    },
                },
            },
            "MuiChip": {
                "styleOverrides": {
                    "root": {
                        "borderRadius": "4px",
                    },
                    "colorPrimary": {
                        "backgroundColor": colors.primary["main"],
                        "color": colors.primary["contrast"],
                        "&:hover": {
                            "backgroundColor": colors.primary["hover"],
                        },
                    },
                    "colorSecondary": {
                        "backgroundColor": colors.secondary["main"],
                        "color": colors.secondary["contrast"],
                        "&:hover": {
                            "backgroundColor": colors.secondary["hover"],
                        },
                    },
                },
            },
            "MuiTextField": {
                "styleOverrides": {
                    "root": {
                        "& .MuiOutlinedInput-root": {
                            "&:hover .MuiOutlinedInput-notchedOutline": {
                                "borderColor": colors.dynamic["main"],
                            },
                            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                                "borderColor": colors.dynamic["main"],
                                "borderWidth": "2px",
                            },
                            "& fieldset": {
                                "borderColor": colors.border["std"],
                            },
                        },
                    },
                },
            },
            "MuiPaper": {
                "styleOverrides": {
                    "root": {
                        "backgroundColor": colors.background["paper"],
                    },
                },
            },
            "MuiButtonBase": {
                "defaultProps": {
                    "disableRipple": True,
                },
            },
            "MuiAppBar": {
                "defaultProps": {"enableColorOnDark": True, "color": "primary"},
                "styleOverrides": {
                    "root": {
                        "backgroundColor": colors.background["surface"],
                        "color": colors.text["primary"],
                    },
                },
            },
        },
        "typography": {
            "fontFamily": '"Siemens Sans", "Arial", sans-serif',
            "h1": {
                "fontWeight": 700,
                "fontSize": "1.8125rem",
                "lineHeight": 1.2,
            },
            "h2": {
                "fontWeight": 700,
                "fontSize": "1.5rem",
                "lineHeight": 1.43,
            },
            "h3": {
                "fontWeight": 700,
                "fontSize": "1.25rem",
                "lineHeight": 1.5,
            },
            "h4": {
                "fontWeight": 700,
                "fontSize": "1.rem",
                "lineHeight": 1.5,
            },
            "h5": {
                "fontWeight": 700,
                "fontSize": "0.875rem",
                "lineHeight": 1.43,
            },
            "h6": {
                "fontWeight": 700,
                "fontSize": "0.75rem",
                "lineHeight": 1.5,
            },
            "body1": {
                "fontWeight": 400,
                "fontSize": "1rem",
                "lineHeight": 1.50,
            },
            "body2": {
                "fontSize": "0.875rem",
                "lineHeight": 1.43,
            },
            "button": {
                "fontWeight": 700,
                "textTransform": "none",
                "fontSize": "1rem",
                "lineHeight": 1.75,
            },
            "caption": {
                "fontSize": "0.75rem",
                "lineHeight": 1.66,
            },
        },
        "shape": {
            "borderRadius": 2,
        },
        "spacing": 8,  # 8px base spacing unit
        
    }


# Convenience aliases
siemens_ix_light_theme = create_theme("light")
siemens_ix_dark_theme = create_theme("dark")


__all__ = [
    "create_theme",
    "siemens_ix_light_theme",
    "siemens_ix_dark_theme",
]
