"""Spritesheet utility module.

This module provides functionality for extracting individual sprites
or tiles from a larger spritesheet image represented as a NumPy array.
"""

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)


class Spritesheet:
    """Spritesheet image handler.

    This class provides methods for extracting tiles from a spritesheet
    image while automatically trimming transparent padding around the
    extracted sprite.

    Attributes:
        img_3d: Source spritesheet image represented as
            a three-dimensional RGBA NumPy array.
    """

    def __init__(self, three_dimension_img: np.ndarray) -> None:
        """Initialize the spritesheet handler.

        Args:
            three_dimension_img: Spritesheet image stored as
                a three-dimensional RGBA NumPy array.
        """
        self.img_3d = three_dimension_img

    def get_tileset(
            self,
            x_min: int, x_max: int,
            y_min: int, y_max: int
    ) -> np.ndarray:
        """Extract and crop a tile from the spritesheet.

        Extracts a rectangular region from the spritesheet and removes any
        fully transparent border pixels surrounding the visible sprite.

        Args:
            x_min: Left boundary of the tile region.
            x_max: Right boundary of the tile region.
            y_min: Upper boundary of the tile region.
            y_max: Lower boundary of the tile region.

        Returns:
            np.ndarray: Cropped sprite image containing only the visible
            portion of the extracted tile.
        """
        tileset = self.img_3d[y_min:y_max, x_min:x_max]
        tile_mask = tileset[:, :, 3] > 0
        rows, cols = np.where(tile_mask)
        start_x, end_x = (min(cols), max(cols))
        start_y, end_y = (min(rows), max(rows))
        final_tile = tileset[start_y:end_y + 1, start_x:end_x + 1]
        return (final_tile)
