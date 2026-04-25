class Pattern42Error(Exception):
    pass


class Pattern42:

    _DIGIT_4: list[list[int]] = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 1],
    ]

    _DIGIT_2: list[list[int]] = [
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0]
    ]

    _CELL_WIDTH = 9
    _CELL_HEIGHT = 5

    @classmethod
    def create_grid_42pattern(
        cls,
        val_width: int,
        val_height: int
    ) -> list[list[int]]:
        width: int = (2 * val_width) + 1
        height: int = (2 * val_height) + 1

        if width <= 0:
            raise Pattern42Error(f"Invalid width {width}")
        if height <= 0:
            raise Pattern42Error(f"Invalid height {height}")

        if width < Pattern42._CELL_WIDTH or height < Pattern42._CELL_HEIGHT:
            raise Pattern42Error("Size to small for 42 pattern")
        grid: list[list[int]] = [
            [1 for _ in range(width)]
            for _ in range(height)
        ]

        offset_x = (val_width - Pattern42._CELL_WIDTH) // 2
        offset_y = (val_height - Pattern42._CELL_HEIGHT) // 2

        for row in range(5):
            for col in range(4):
                if Pattern42._DIGIT_4[row][col] == 1:
                    gx = (offset_x + col) * 2 + 1
                    gy = (offset_y + row) * 2 + 1
                    grid[gy][gx] = 2

                if Pattern42._DIGIT_2[row][col] == 1:
                    gx = (offset_x + col + 4) * 2 + 1
                    gy = (offset_y + row) * 2 + 1
                    grid[gy][gx] = 2

        return grid

    @classmethod
    def get_42_width(cls) -> int:
        return (cls._CELL_WIDTH)

    @classmethod
    def get_42_height(cls) -> int:
        return (cls._CELL_HEIGHT)
