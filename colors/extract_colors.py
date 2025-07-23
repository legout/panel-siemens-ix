#!/usr/bin/env python3
"""
Extract color variables from SCSS files and convert to Python dictionary.
"""

import re
import json
from typing import Dict, Union, Tuple

def hex_to_rgba(hex_color: str) -> str:
    """Convert hex color to rgba format."""
    hex_color = hex_color.lstrip('#')
    
    # Handle 3-digit hex
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Handle 4-digit hex (with alpha)
    if len(hex_color) == 4:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Handle 6-digit hex
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, 1)"
    
    # Handle 8-digit hex (with alpha)
    if len(hex_color) == 8:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16) / 255
        return f"rgba({r}, {g}, {b}, {a:.2f})"
    
    return hex_color

def rgba_to_hex(rgba_str: str) -> str:
    """Convert rgba color to hex format."""
    rgba_match = re.match(r'rgba?\(([^)]+)\)', rgba_str)
    if not rgba_match:
        return rgba_str
    
    values = rgba_match.group(1).split(',')
    values = [v.strip() for v in values]
    
    r = int(values[0])
    g = int(values[1])
    b = int(values[2])
    
    if len(values) == 4:
        a = float(values[3])
        if a == 1:
            return f"#{r:02x}{g:02x}{b:02x}"
        else:
            alpha_hex = int(a * 255)
            return f"#{r:02x}{g:02x}{b:02x}{alpha_hex:02x}"
    
    return f"#{r:02x}{g:02x}{b:02x}"

def parse_color_value(color_str: str) -> str:
    """Parse color value and return in appropriate format."""
    color_str = color_str.strip()
    
    # Handle rgba format
    if color_str.startswith('rgba('):
        return rgba_to_hex(color_str)
    
    # Handle hex format
    if color_str.startswith('#'):
        return color_str
    
    # Handle var() references - return as-is
    if color_str.startswith('var('):
        return color_str
    
    return color_str

def extract_colors_from_scss(file_path: str) -> Dict[str, str]:
    """Extract color variables from SCSS file."""
    colors = {}
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all CSS custom properties with --theme-color- prefix
    pattern = r'--theme-color-([^:]+):\s*([^;]+);'
    matches = re.findall(pattern, content)
    
    for name, value in matches:
        # Remove the prefix and clean the name
        clean_name = name.strip()
        clean_value = parse_color_value(value)
        
        # Skip if it's a var() reference
        if clean_value.startswith('var('):
            continue
            
        colors[clean_name] = clean_value
    
    return colors

def main():
    """Main function to extract colors from colors_light.scss."""
    scss_file = 'css/colors_light.scss'
    
    try:
        colors = extract_colors_from_scss(scss_file)
        
        # Convert to JSON and print
        print(json.dumps(colors, indent=2))
        
        # Also save to file
        with open('colors_light_dict.json', 'w') as f:
            json.dump(colors, f, indent=2)
        
        print(f"\nExtracted {len(colors)} color variables from {scss_file}")
        print("Saved to colors_light_dict.json")
        
    except FileNotFoundError:
        print(f"Error: {scss_file} not found")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()