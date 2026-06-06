# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer_utils.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/24 11:42:36 by ialrandr        #+#    #+#               #
#  Updated: 2026/06/06 19:42:41 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

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
    x_min, x_max = x_coordinates
    y_min, y_max = y_coordinates
    tileset = spritesheet.get_tileset(
                x_min,
                x_max,
                y_min,
                y_max
            )
    tileset_height, tileset_witdth, _ = tileset.shape
    return (tileset.copy(), tileset_height, tileset_witdth)


def scale_pixel(sprite: np.ndarray, scale: int) -> np.ndarray:
    scaled_img = np.repeat(sprite, scale, axis=0)
    scaled_img = np.repeat(scaled_img, scale, axis=1)

    return (scaled_img)


def recolor_pixel(
        sprite: np.ndarray,
        target_color: list[int],
        new_color: list[int]
) -> None:

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
        [189, 175, 179, 255],
    ],

    "bright_theme": [
        [41, 89, 165, 255],
        [41 - 10, 89 - 10, 165 - 10, 255],
        [41 - 20, 89 - 20, 165 - 20, 255],
    ],

    "green_theme": [
        [80, 66, 30, 255],
        [223, 223, 223, 255],
        [204, 228, 176, 255],
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
        [12, 76, 200, 255],
        [180, 196, 254, 255],
        [9, 76, 200, 255]
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
    "bright_theme": [153, 253, 254, 255],
    "green_theme": [72, 90, 40, 255],
}
