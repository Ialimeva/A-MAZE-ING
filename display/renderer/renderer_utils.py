"""Sprite and theme utility module.

This module provides helper functions for extracting, scaling, and
recoloring sprite images. It also defines the color themes used for
maze floors, walls, and background rendering.
"""

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

from .spritsheet import Spritesheet


def tileset(
            x_coordinates: tuple[int, int],
            y_coordinates: tuple[int, int],
            spritesheet: Spritesheet
        ) -> tuple[np.ndarray, int, int]:
    """Extract a sprite from a spritesheet.

    Retrieves a sprite using the specified coordinate bounds and
    returns a copy of the sprite along with its dimensions.

    Args:
        x_coordinates: Horizontal bounds of the
            sprite in the spritesheet.
        y_coordinates: Vertical bounds of the
            sprite in the spritesheet.
        spritesheet: Source spritesheet object.

    Returns:
        tuple:
            A tuple containing:

            - The extracted sprite image.
            - Sprite height.
            - Sprite width.
    """
    x_min, x_max = x_coordinates
    y_min, y_max = y_coordinates
    tileset = spritesheet.get_tileset(
                x_min,
                x_max,
                y_min,
                y_max
            )
    tileset_height, tileset_width, _ = tileset.shape
    return (tileset.copy(), tileset_height, tileset_width)


def scale_pixel(sprite: np.ndarray, scale: int) -> np.ndarray:
    """Scale a sprite using nearest-neighbor enlargement.

    Each pixel in the source image is duplicated horizontally and
    vertically according to the specified scale factor.

    Args:
        sprite: Sprite image to scale.
        scale: Scaling factor.

    Returns:
        np.ndarray: Scaled sprite image.
    """
    scaled_img = np.repeat(sprite, scale, axis=0)
    scaled_img = np.repeat(scaled_img, scale, axis=1)

    return (scaled_img)


def recolor_pixel(
        sprite: np.ndarray,
        target_color: list[int],
        new_color: list[int]
) -> None:
    """Replace a color within a sprite.

    Finds all pixels matching the target color and replaces them
    with the specified new color.

    Args:
        sprite: Sprite image to modify.
        target_color: RGBA color to replace.
        new_color: Replacement RGBA color.
    """
    mask = np.all(sprite == target_color, axis=2)
    sprite[mask] = new_color


floor_colors: dict[str, list[list[int]]] = {
    "default_theme": [
        [143, 164, 194, 255],
        [215, 240, 246, 255],
        [83, 57, 133, 255]
    ],

    "ice_theme": [
        [110, 68, 55, 255],
        [221, 222, 203, 255],
        [228, 169, 61, 255],
    ],

    "bright_theme": [
        [21, 69, 145, 255],
        [129, 203, 255, 255],
        [119, 183, 255, 255],
    ],

    "green_theme": [
        [80, 66, 30, 255],
        [223, 223, 223, 255],
        [167, 221, 185, 255],
    ],
}

wall_colors: dict[str, list[list[int]]] = {
    "default_theme": [
        [53, 40, 66, 255],
        [23, 17, 28, 255],
        [96, 103, 117, 255]
    ],

    "ice_theme": [
        [92, 43, 35, 255],
        [228, 169, 61, 255],
        [253, 254, 254, 255],
    ],

    "bright_theme": [
        [31, 79, 155, 255],
        [99, 173, 255, 255],
        [255, 255, 255, 255]
    ],

    "green_theme": [
        [80, 66, 30, 255],
        [167, 221, 185, 255],
        [255, 255, 255, 255]
    ]
}

background_colors: dict[str, list[int]] = {
    "default_theme": [46, 37, 79, 255],
    "ice_theme": [233, 235, 193, 255],
    "bright_theme": [99, 173, 255, 255],
    "green_theme": [72, 90, 40, 255],
}
