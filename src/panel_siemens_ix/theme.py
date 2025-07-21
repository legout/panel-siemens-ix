"""
Siemens iX Theme for panel-material-ui

This module provides a Material-UI compatible theme based on the Siemens iX design system,
supporting both light and dark modes with comprehensive color definitions including 
hover and active states.
"""

from typing import Dict, Any, Optional


def _hex_to_rgba(hex_color: str, alpha: Optional[float] = None) -> str:
    """Convert hex color to rgba format, optionally with custom alpha."""
    hex_color = hex_color.lstrip('#')
    
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
SIEMENS_IX_DARK_COLORS = {
    # Primary Colors
    'primary': {
        'main': '#00cccc',
        'hover': '#00ffb9',
        'active': '#00e5aa',
        'contrast': '#000028',
        'disabled': '#00cccc73',
    },
    
    # Dynamic Colors (Interactive elements)
    'dynamic': {
        'main': '#00ffb9',
        'hover': '#62eec7',
        'active': '#5ce0bc',
        'contrast': '#000028',
    },
    
    # Secondary Colors
    'secondary': {
        'main': '#000028',
        'hover': '#001f39',
        'active': '#00182b',
        'contrast': '#ffffff',
    },
    
    # Text Colors
    'text': {
        'primary': '#ffffff',        # Standard text
        'secondary': '#ffffff99',    # Soft text (60% opacity)
        'disabled': 'rgba(255,255,255,0.45)',  # Weak text (45% opacity)
        'hint': '#ffffff99',
    },
    
    # Background Colors
    'background': {
        'default': '#000028',
        'paper': '#23233c',
        'surface': '#37374d',
    },
    
    # Status Colors
    'error': {
        'main': '#ff2640',
        'hover': '#ff4259',
        'active': '#ff1431',
        'contrast': '#000028',
    },
    'warning': {
        'main': '#ffd732',
        'hover': '#ffdd52',
        'active': '#ffd424',
        'contrast': '#000028',
    },
    'info': {
        'main': '#00bedc',
        'hover': '#00cff0',
        'active': '#00b5d1',
        'contrast': '#000028',
    },
    'success': {
        'main': '#01d65a',
        'hover': '#01ea62',
        'active': '#01c151',
        'contrast': '#000028',
    },
}

# Siemens iX Color Palette - Light Theme
SIEMENS_IX_LIGHT_COLORS = {
    # Primary Colors
    'primary': {
        'main': '#007993',
        'hover': '#196269',
        'active': '#16565c',
        'contrast': '#ffffff',
        'disabled': '#0079934d',
    },
    
    # Dynamic Colors (Interactive elements)
    'dynamic': {
        'main': '#005159',
        'hover': '#125d65',
        'active': '#105259',
        'contrast': '#ffffff',
    },
    
    # Secondary Colors
    'secondary': {
        'main': '#ffffff',
        'hover': '#d1fff2',
        'active': '#b8f2e2',
        'contrast': '#000028',
    },
    
    # Text Colors
    'text': {
        'primary': '#000028',        # Standard text
        'secondary': '#00002899',    # Soft text (60% opacity)
        'disabled': '#0000284d',     # Weak text (30% opacity)
        'hint': '#00002899',
    },
    
    # Background Colors
    'background': {
        'default': '#ffffff',
        'paper': '#f3f3f0',
        'surface': '#e8e8e3',
    },
    
    # Status Colors
    'error': {
        'main': '#d72339',
        'hover': '#c11f33',
        'active': '#b41d30',
        'contrast': '#ffffff',
    },
    'warning': {
        'main': '#e9c32a',
        'hover': '#e3ba17',
        'active': '#d0ab15',
        'contrast': '#000028',
    },
    'info': {
        'main': '#007eb1',
        'hover': '#00719e',
        'active': '#006994',
        'contrast': '#ffffff',
    },
    'success': {
        'main': '#01893a',
        'hover': '#017a33',
        'active': '#016f2f',
        'contrast': '#ffffff',
    },
}


def create_siemens_ix_theme(mode: str = 'light') -> Dict[str, Any]:
    """
    Create a Material-UI compatible theme using Siemens iX design system colors.
    
    Args:
        mode: Theme mode, either 'light' or 'dark'
        
    Returns:
        Dictionary containing Material-UI theme configuration
        
    Raises:
        ValueError: If mode is not 'light' or 'dark'
    """
    if mode not in ['light', 'dark']:
        raise ValueError("Mode must be either 'light' or 'dark'")
    
    colors = SIEMENS_IX_DARK_COLORS if mode == 'dark' else SIEMENS_IX_LIGHT_COLORS
    
    return {
        'palette': {
            'mode': mode,
            'primary': {
                'main': colors['primary']['main'],
                'dark': colors['primary']['active'],
                'light': colors['primary']['hover'],
                'contrastText': colors['primary']['contrast'],
            },
            'secondary': {
                'main': colors['dynamic']['main'],  # Use dynamic color for secondary
                'dark': colors['dynamic']['active'],
                'light': colors['dynamic']['hover'],
                'contrastText': colors['dynamic']['contrast'],
            },
            'error': {
                'main': colors['error']['main'],
                'dark': colors['error']['active'],
                'light': colors['error']['hover'],
                'contrastText': colors['error']['contrast'],
            },
            'warning': {
                'main': colors['warning']['main'],
                'dark': colors['warning']['active'],
                'light': colors['warning']['hover'],
                'contrastText': colors['warning']['contrast'],
            },
            'info': {
                'main': colors['info']['main'],
                'dark': colors['info']['active'],
                'light': colors['info']['hover'],
                'contrastText': colors['info']['contrast'],
            },
            'success': {
                'main': colors['success']['main'],
                'dark': colors['success']['active'],
                'light': colors['success']['hover'],
                'contrastText': colors['success']['contrast'],
            },
            'text': {
                'primary': colors['text']['primary'],
                'secondary': colors['text']['secondary'],
                'disabled': colors['text']['disabled'],
                'hint': colors['text']['hint'],
            },
            'background': {
                'default': colors['background']['default'],
                'paper': colors['background']['paper'],
            },
            'divider': colors['text']['disabled'],
        },
        'components': {
            'MuiButton': {
                'styleOverrides': {
                    'root': {
                        'textTransform': 'none',  # Siemens iX typically uses sentence case
                        'borderRadius': '4px',
                    },
                    'containedPrimary': {
                        '&:hover': {
                            'backgroundColor': colors['primary']['hover'],
                        },
                        '&:active': {
                            'backgroundColor': colors['primary']['active'],
                        },
                    },
                    'containedSecondary': {
                        'backgroundColor': colors['dynamic']['main'],
                        'color': colors['dynamic']['contrast'],
                        '&:hover': {
                            'backgroundColor': colors['dynamic']['hover'],
                        },
                        '&:active': {
                            'backgroundColor': colors['dynamic']['active'],
                        },
                    },
                },
            },
            'MuiChip': {
                'styleOverrides': {
                    'root': {
                        'borderRadius': '16px',
                    },
                    'colorPrimary': {
                        'backgroundColor': colors['primary']['main'],
                        'color': colors['primary']['contrast'],
                        '&:hover': {
                            'backgroundColor': colors['primary']['hover'],
                        },
                    },
                },
            },
            'MuiTextField': {
                'styleOverrides': {
                    'root': {
                        '& .MuiOutlinedInput-root': {
                            '&:hover .MuiOutlinedInput-notchedOutline': {
                                'borderColor': colors['dynamic']['main'],
                            },
                            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                                'borderColor': colors['dynamic']['main'],
                            },
                        },
                    },
                },
            },
        },
        'typography': {
            'fontFamily': '"Siemens Sans", "Arial", sans-serif',
            'h1': {
                'fontWeight': 600,
            },
            'h2': {
                'fontWeight': 600,
            },
            'h3': {
                'fontWeight': 600,
            },
            'h4': {
                'fontWeight': 600,
            },
            'h5': {
                'fontWeight': 600,
            },
            'h6': {
                'fontWeight': 600,
            },
            'button': {
                'fontWeight': 500,
                'textTransform': 'none',
            },
        },
        'shape': {
            'borderRadius': 4,
        },
        'spacing': 8,  # 8px base spacing unit
    }


def get_siemens_ix_colors(mode: str = 'light') -> Dict[str, Any]:
    """
    Get the raw Siemens iX color palette for the specified mode.
    
    Args:
        mode: Theme mode, either 'light' or 'dark'
        
    Returns:
        Dictionary containing the color palette
        
    Raises:
        ValueError: If mode is not 'light' or 'dark'
    """
    if mode not in ['light', 'dark']:
        raise ValueError("Mode must be either 'light' or 'dark'")
    
    return SIEMENS_IX_DARK_COLORS if mode == 'dark' else SIEMENS_IX_LIGHT_COLORS


# Convenience aliases
siemens_ix_light_theme = lambda: create_siemens_ix_theme('light')
siemens_ix_dark_theme = lambda: create_siemens_ix_theme('dark')


__all__ = [
    'create_siemens_ix_theme',
    'get_siemens_ix_colors',
    'siemens_ix_light_theme',
    'siemens_ix_dark_theme',
    'SIEMENS_IX_DARK_COLORS',
    'SIEMENS_IX_LIGHT_COLORS',
]