# Predefined color maps
import panel_material_ui as pmui
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict


def _hex_to_rgba(color: str, alpha: Optional[float] = None) -> str:
    """
    Convert hex or rgba color to rgba format, optionally with custom alpha.

    Args:
        color: Hex color (e.g., '#00cccc') or rgba string (e.g., 'rgba(0, 204, 204, 0.45)')
        alpha: Optional alpha value to override existing alpha

    Returns:
        rgba color string
    """
    # Handle existing rgba strings
    if color.startswith("rgba("):
        if alpha is not None:
            # Extract rgb values and apply new alpha
            import re

            match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)", color)
            if match:
                r, g, b = match.groups()
                return f"rgba({r}, {g}, {b}, {alpha})"
        return color

    # Handle hex colors
    hex_color = color.lstrip("#")

    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    elif len(hex_color) == 3:
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
    else:
        raise ValueError(f"Invalid hex color format: {hex_color}")

    if alpha is not None:
        return f"rgba({r}, {g}, {b}, {alpha})"
    return f"rgb({r}, {g}, {b})"


# Siemens iX Color Palette - Dark Theme
@dataclass(frozen=True)
class SiemensIXDarkColors:
    primary: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#00cccc",
            "hover": "#00ffb9",
            "active": "#00e5aa",
            "contrast": "#000028",
            "disabled": "#00cccc73",
        }
    )
    dynamic: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#00ffb9",
            "hover": "#62eec7",
            "active": "#5ce0bc",
            "contrast": "#000028",
        }
    )
    secondary: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#000028",
            "hover": "#001f39",
            "active": "#00182b",
            "contrast": "#ffffff",
        }
    )
    text: Dict[str, str] = field(
        default_factory=lambda: {
            "primary": "#ffffff",
            "secondary": "#ffffff99",
            "disabled": "rgba(255,255,255,0.45)",
            "hint": "#ffffff99",
        }
    )
    background: Dict[str, str] = field(
        default_factory=lambda: {
            "default": "#000028",
            "paper": "#23233c",
            "surface": "#37374d",
        }
    )
    error: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#ff2640",
            "hover": "#ff4259",
            "active": "#ff1431",
            "contrast": "#000028",
        }
    )
    warning: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#ffd732",
            "hover": "#ffdd52",
            "active": "#ffd424",
            "contrast": "#000028",
        }
    )
    info: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#00bedc",
            "hover": "#00cff0",
            "active": "#00b5d1",
            "contrast": "#000028",
        }
    )
    success: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#01d65a",
            "hover": "#01ea62",
            "active": "#01c151",
            "contrast": "#000028",
        }
    )
    ghost: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#ffffff00",
            "hover": "#9d9d9626",
            "active": "#69696326",
            "selected": "#00ffb91f",
            "selected-hover": "#68fdbf38",
            "selected-active": "#73ddaf38",
        }
    )
    component: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#9d9d9633",
            "2": "#ffffff26",
            "3": "#ffffff4d",
            "4": "#ffffff73",
            "5": "#ffffff99",
            "6": "#ffffffbf",
        }
    )
    border: Dict[str, str] = field(
        default_factory=lambda: {
            "std": "#e8e8e38c",
            "soft": "#ebf0f566",
            "weak": "#e8e8e326",
            "x-weak": "#9d9d9633",
            "focus": "#1491EB",
            "contrast": "#ffffff",
            "hard": "#b3b3be",
        }
    )
    neutral: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#b9b9b6",
            "hover": "#cbcbc8",
            "active": "#afafac",
            "contrast": "#000028",
        }
    )
    shadow: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#00000099",
            "2": "#000000",
            "3": "#00000099",
        }
    )

    chart: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#00ffb9",
            "1-40": "#00ffb966",
            "2": "#85E9D2",
            "2-40": "#85E9D266",
            "3": "#00C1B6",
            "3-40": "#00C1B666",
            "4": "#CCF5F5",
            "4-40": "#CCF5F566",
            "5": "#7D8099",
            "5-40": "#7D809966",
            "6": "#6895F6",
            "6-40": "#6895F666",
            "7": "#97C7FF",
            "7-40": "#97C7FF66",
            "8": "#3664C6",
            "8-40": "#3664C666",
            "9": "#BFB0F3",
            "9-40": "#BFB0F366",
            "10": "#805CFF",
            "10-40": "#805CFF66",
            "11": "#B95CC9",
            "11-40": "#B95CC966",
            "12": "#E5659B",
            "12-40": "#E5659B66",
            "13": "#FF98C4",
            "13-40": "#FF98C466",
            "14": "#BE5925",
            "14-40": "#BE592566",
            "15": "#FFBC66",
            "15-40": "#FFBC6666",
            "16": "#FFF7D6",
            "16-40": "#FFF7D666",
            "17": "#AAAA96",
            "17-40": "#AAAA9666",
        }
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Siemens iX Color Palette - Light Theme
@dataclass(frozen=True)
class SiemensIXLightColors:
    primary: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#007993",
            "hover": "#196269",
            "active": "#16565c",
            "contrast": "#ffffff",
            "disabled": "#0079934d",
        }
    )
    dynamic: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#005159",
            "hover": "#125d65",
            "active": "#105259",
            "contrast": "#ffffff",
        }
    )
    secondary: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#ffffff",
            "hover": "#d1fff2",
            "active": "#b8f2e2",
            "contrast": "#000028",
        }
    )
    text: Dict[str, str] = field(
        default_factory=lambda: {
            "primary": "#000028",
            "secondary": "#00002899",
            "disabled": "#0000284d",
            "hint": "#00002899",
        }
    )
    background: Dict[str, str] = field(
        default_factory=lambda: {
            "default": "#ffffff",
            "paper": "#f3f3f0",
            "surface": "#e8e8e3",
        }
    )
    error: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#d72339",
            "hover": "#c11f33",
            "active": "#b41d30",
            "contrast": "#ffffff",
        }
    )
    warning: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#e9c32a",
            "hover": "#e3ba17",
            "active": "#d0ab15",
            "contrast": "#000028",
        }
    )
    info: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#007eb1",
            "hover": "#00719e",
            "active": "#006994",
            "contrast": "#ffffff",
        }
    )
    success: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#01893a",
            "hover": "#017a33",
            "active": "#016f2f",
            "contrast": "#ffffff",
        }
    )
    ghost: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#00002800",
            "hover": "#bdbdae26",
            "active": "#8f8f7526",
            "selected": "#00ffb92e",
            "selected-hover": "#20c57e38",
            "selected-active": "#009e6738",
        }
    )
    component: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#bdbdae33",
            "2": "#0000281a",
            "3": "#00002833",
            "4": "#0000284d",
            "5": "#00002873",
            "6": "#00002899",
        }
    )
    border: Dict[str, str] = field(
        default_factory=lambda: {
            "std": "#0000284d",
            "soft": "#00002833",
            "weak": "#23233c26",
            "x-weak": "#bdbdae33",
            "focus": "#1491EB",
            "contrast": "#000028",
            "hard": "#4c4c68",
        }
    )
    neutral: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "#66667e",
            "hover": "#5b5b71",
            "active": "#545468",
            "contrast": "#ffffff",
        }
    )
    shadow: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#0000281a",
            "2": "#00002833",
            "3": "#0000281e",
        }
    )
    chart: Dict[str, str] = field(
        default_factory=lambda: {
            "1": "#1a747d",
            "1-40": "#1a747d66",
            "2": "#005159",
            "2-40": "#00515966",
            "3": "#009999",
            "3-40": "#00999966",
            "4": "#002949",
            "4-40": "#00294966",
            "5": "#4c4c68",
            "5-40": "#4c4c6866",
            "6": "#3664c6",
            "6-40": "#3664c666",
            "7": "#00237a",
            "7-40": "#00237a66",
            "8": "#00004a",
            "8-40": "#00004a66",
            "9": "#553ba3",
            "9-40": "#553ba366",
            "10": "#7353e5",
            "10-40": "#7353e566",
            "11": "#740089",
            "11-40": "#74008966",
            "12": "#c04774",
            "12-40": "#c0477466",
            "13": "#4f153d",
            "13-40": "#4f153d66",
            "14": "#be5925",
            "14-40": "#be592566",
            "15": "#801100",
            "15-40": "#80110066",
            "16": "#805800",
            "16-40": "#80580066",
            "17": "#5e5e4a",
            "17-40": "#5e5e4a66",
        }
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def get_colors(mode: str = "light") -> SiemensIXDarkColors | SiemensIXLightColors:
    """
    Get the raw Siemens iX color palette for the specified mode.

    Args:
        mode: Theme mode, either 'light' or 'dark'

    Returns:
        Dictionary containing the color palette

    Raises:
        ValueError: If mode is not 'light' or 'dark'
    """
    if mode not in ["light", "dark"]:
        raise ValueError("Mode must be either 'light' or 'dark'")

    return SiemensIXDarkColors() if mode == "dark" else SiemensIXLightColors()


def get_continuous_cmap(dark_theme: bool = False, n_colors: int = 128) -> List[str]:
    """
    Get the continuous color map based on the dark theme flag.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color map. Otherwise, return light theme color map.

    Returns
    -------
    List[str]
        List of hex color codes forming a continuous color map
    """
    colors = get_colors("dark" if dark_theme else "light")
    return pmui.theme.linear_gradient(colors.background["surface"], colors.primary["main"], n=n_colors)


def get_categorical_palette(
    dark_theme: bool = False,
    n_colors: int = 17,
    primary: bool = False,
    opacity: bool = False,
) -> List[str]:
    """
    Get a categorical color palette based on the dark theme flag.

    For small palettes (n_colors <= 5), returns the theme's main colors.
    For larger palettes, generates additional colors based on the primary color.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color palette. Otherwise, return light theme color palette.
    n_colors : int, default=20
        Number of colors in the returned palette.

    Returns
    -------
    List[str]
        List of hex color codes suitable for categorical data
    """
    colors = get_colors("dark" if dark_theme else "light")

    if primary:
        return pmui.theme.generate_palette(
            color=colors.primary["main"], n_colors=n_colors
        )

    palette_all = colors.chart
    color_sequence = [3, 2, 8, 1, 6, 4, 10, 9, 11, 14, 13, 12, 7, 15, 16, 17, 5]
    palette_40 = [palette_all[f"{k}-40"] for k in color_sequence]
    palette = [palette_all[f"{k}"] for k in color_sequence]

    if n_colors <= len(palette):
        if opacity:
            return palette_40[:: max(17 // max(1,n_colors), 1)]
        return palette[:: max(17 // max(1,n_colors), 1)]

    return pmui.theme.generate_palette(colors.primary["main"], n_colors=n_colors)


__all__ = [
    "SiemensIXDarkColors",
    "SiemensIXLightColors",
    "get_colors",
    "get_continuous_cmap",
    "get_categorical_palette",
    "_hex_to_rgba",
]
