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
            # Primary and brand colors - bright and vibrant for dark background
            "1": "#00ffb9",  # Bright cyan (primary accent)
            "1-40": "#00ffb966",
            "2": "#00e5d4",  # Light cyan
            "2-40": "#00e5d466",
            "3": "#85E9D2",  # Mint
            "3-40": "#85E9D266",
            # Blues and purples
            "4": "#6895F6",  # Bright blue
            "4-40": "#6895F666",
            "5": "#97C7FF",  # Light blue
            "5-40": "#97C7FF66",
            "6": "#3664C6",  # Medium blue
            "6-40": "#3664C666",
            "7": "#805CFF",  # Purple
            "7-40": "#805CFF66",
            "8": "#BFB0F3",  # Light purple
            "8-40": "#BFB0F366",
            # Warmer colors
            "9": "#FF98C4",  # Pink
            "9-40": "#FF98C466",
            "10": "#E5659B",  # Rose
            "10-40": "#E5659B66",
            "11": "#B95CC9",  # Magenta
            "11-40": "#B95CC966",
            # Oranges and yellows
            "12": "#FFBC66",  # Peach
            "12-40": "#FFBC6666",
            "13": "#FFF7D6",  # Light yellow
            "13-40": "#FFF7D666",
            "14": "#BE5925",  # Orange
            "14-40": "#BE592566",
            # Neutral and supporting colors
            "15": "#7D8099",  # Blue-gray
            "15-40": "#7D809966",
            "16": "#AAAA96",  # Sage green
            "16-40": "#AAAA9666",
            "17": "#00C1B6",  # Teal (connector color)
            "17-40": "#00C1B666",
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
            # Primary and brand colors - deeper and more saturated for light background
            "1": "#007993",  # Primary blue
            "1-40": "#00799366",
            "2": "#005159",  # Dark teal
            "2-40": "#00515966",
            "3": "#009999",  # Medium teal
            "3-40": "#00999966",
            # Blues and purples - darker for better contrast
            "4": "#3664c6",  # Strong blue
            "4-40": "#3664c666",
            "5": "#00237a",  # Navy blue
            "5-40": "#00237a66",
            "6": "#00004a",  # Deep blue
            "6-40": "#00004a66",
            "7": "#553ba3",  # Purple
            "7-40": "#553ba366",
            "8": "#7353e5",  # Lighter purple
            "8-40": "#7353e566",
            # Warmer colors - deeper and more saturated
            "9": "#c04774",  # Rose
            "9-40": "#c0477466",
            "10": "#740089",  # Magenta
            "10-40": "#74008966",
            "11": "#4f153d",  # Dark red
            "11-40": "#4f153d66",
            # Oranges and yellows - darker for visibility
            "12": "#be5925",  # Orange
            "12-40": "#be592566",
            "13": "#801100",  # Dark orange
            "13-40": "#80110066",
            "14": "#805800",  # Olive
            "14-40": "#80580066",
            # Neutral and supporting colors
            "15": "#4c4c68",  # Blue-gray
            "15-40": "#4c4c6866",
            "16": "#002949",  # Very dark blue
            "16-40": "#00294966",
            "17": "#5e5e4a",  # Sage green
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
    Get the continuous color map optimized for the Siemens iX design system.

    Creates a perceptually uniform gradient that transitions smoothly from
    the surface background through accent colors to create a professional,
    Siemens iX-branded continuous colormap.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color map. Otherwise, return light theme color map.
    n_colors : int, default=128
        Number of colors in the continuous gradient.

    Returns
    -------
    List[str]
        List of hex color codes forming a continuous color map

    Examples
    --------
    >>> # Get a light theme continuous colormap
    >>> cmap_light = get_continuous_cmap(dark_theme=False, n_colors=64)

    >>> # Get a dark theme continuous colormap
    >>> cmap_dark = get_continuous_cmap(dark_theme=True, n_colors=64)
    """
    colors = get_colors("dark" if dark_theme else "light")

    if dark_theme:
        # Dark theme: gradient from surface dark cyan through bright accent
        # Start with surface, go through mid-tone, end with bright accent
        start_color = colors.background["surface"]  # #37374d
        mid_color = colors.chart["17"]  # #00C1B6 (teal connector)
        end_color = colors.primary["main"]  # #00cccc

        # Create a three-part gradient for better visual distribution
        n_part1 = n_colors // 3
        n_part2 = n_colors // 3
        n_part3 = n_colors - n_part1 - n_part2

        part1 = pmui.theme.linear_gradient(start_color, mid_color, n=n_part1)
        part2 = pmui.theme.linear_gradient(mid_color, end_color, n=n_part2)
        # For the third part, create variations of the end color
        part3 = pmui.theme.generate_palette(end_color, n_colors=n_part3)

        return part1 + part2 + part3[-n_part3:]
    else:
        # Light theme: gradient from paper through primary to darker shade
        start_color = colors.background["paper"]  # #f3f3f0
        mid_color = colors.primary["main"]  # #007993
        end_color = colors.chart["16"]  # #002949 (very dark blue)

        # Create a three-part gradient for better visual distribution
        n_part1 = n_colors // 3
        n_part2 = n_colors // 3
        n_part3 = n_colors - n_part1 - n_part2

        part1 = pmui.theme.linear_gradient(start_color, mid_color, n=n_part1)
        part2 = pmui.theme.linear_gradient(mid_color, end_color, n=n_part2)
        # For the third part, create darker variations
        part3 = pmui.theme.generate_palette(end_color, n_colors=n_part3)

        return part1 + part2 + part3[-n_part3:]


def get_categorical_palette(
    dark_theme: bool = False,
    n_colors: int = 17,
    primary: bool = False,
    opacity: bool = False,
) -> List[str]:
    """
    Get an optimized categorical color palette for the Siemens iX design system.

    This function provides carefully selected colors that maximize visual distinction
    while maintaining the Siemens iX brand aesthetic. Colors are selected based on
    perceptual distance and theme-appropriate contrast.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color palette. Otherwise, return light theme color palette.
    n_colors : int, default=17
        Number of colors in the returned palette. Must be at least 1.
    primary : bool, default=False
        If True, generate a palette based solely on variations of the primary color.
    opacity : bool, default=False
        If True, return colors with 40% opacity (ending with '-40' in the chart).

    Returns
    -------
    List[str]
        List of hex color codes suitable for categorical data visualization

    Examples
    --------
    >>> # Get a 5-color palette for light theme
    >>> palette = get_categorical_palette(dark_theme=False, n_colors=5)

    >>> # Get a 10-color palette with opacity for dark theme
    >>> palette_opaque = get_categorical_palette(dark_theme=True, n_colors=10, opacity=True)

    >>> # Generate a primary-based palette
    >>> primary_palette = get_categorical_palette(primary=True, n_colors=8)
    """
    if n_colors < 1:
        raise ValueError("n_colors must be at least 1")

    colors = get_colors("dark" if dark_theme else "light")

    # If primary-based palette is requested
    if primary:
        return pmui.theme.generate_palette(
            color=colors.primary["main"], n_colors=n_colors
        )

    # For very small palettes, use semantic colors for better meaning
    if n_colors <= 5:
        semantic_colors = [
            colors.primary["main"],     # Primary
            colors.success["main"],    # Success
            colors.warning["main"],    # Warning
            colors.error["main"],      # Error
            colors.info["main"],       # Info
        ]
        return semantic_colors[:n_colors]

    # Use the enhanced chart colors with improved sequence
    palette_all = colors.chart

    # Improved color sequence for better visual hierarchy
    if dark_theme:
        # Dark theme: start with bright accents, progress through spectrum
        color_sequence = [1, 4, 9, 7, 12, 2, 6, 10, 14, 3, 8, 11, 13, 15, 16, 17, 5]
    else:
        # Light theme: start with primary blues, progress through spectrum
        color_sequence = [1, 4, 7, 9, 12, 2, 6, 10, 14, 3, 8, 11, 13, 15, 16, 17, 5]

    palette = [palette_all[f"{k}"] for k in color_sequence]
    palette_40 = [palette_all[f"{k}-40"] for k in color_sequence]

    # If we have enough predefined colors, sample intelligently
    if n_colors <= len(palette):
        # Use intelligent sampling to get good distribution
        step = max(1, len(palette) // n_colors)
        indices = [i * step for i in range(n_colors)]
        # Ensure we don't go out of bounds
        indices = [min(i, len(palette) - 1) for i in indices]

        if opacity:
            return [palette_40[i] for i in indices]
        else:
            return [palette[i] for i in indices]

    # For more colors than defined, extend using palette generation
    base_colors = palette.copy()

    # Use the most distinct colors as base for generation
    if dark_theme:
        # Use bright colors as base for dark theme
        base_for_generation = [colors.primary["main"], colors.chart["1"], colors.chart["4"]]
    else:
        # Use primary colors as base for light theme
        base_for_generation = [colors.primary["main"], colors.chart["4"], colors.chart["7"]]

    # Generate additional colors
    additional_needed = n_colors - len(base_colors)
    generated_colors = []

    # Distribute generation across base colors
    colors_per_base = max(1, additional_needed // len(base_for_generation))

    for base_color in base_for_generation:
        if len(generated_colors) < additional_needed:
            n_gen = min(colors_per_base, additional_needed - len(generated_colors))
            generated_colors.extend(
                pmui.theme.generate_palette(base_color, n_colors=n_gen + 1)[1:n_gen + 1]
            )

    # Combine and return
    final_palette = base_colors + generated_colors[:additional_needed]
    return final_palette[:n_colors]


__all__ = [
    "SiemensIXDarkColors",
    "SiemensIXLightColors",
    "get_colors",
    "get_continuous_cmap",
    "get_categorical_palette",
    "_hex_to_rgba",
]
