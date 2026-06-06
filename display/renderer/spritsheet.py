import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)


class Spritesheet:
    def __init__(self, three_dimension_img: np.ndarray):
        self.img_3d = three_dimension_img

    def get_tileset(
            self,
            x_min: int, x_max: int,
            y_min: int, y_max: int
    ) -> np.ndarray:
        tileset = self.img_3d[y_min:y_max, x_min:x_max]
        tile_mask = tileset[:, :, 3] > 0
        rows, cols = np.where(tile_mask)
        start_x, end_x = (min(cols), max(cols))
        start_y, end_y = (min(rows), max(rows))
        final_tile = tileset[start_y:end_y + 1, start_x:end_x + 1]
        return (final_tile)
