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
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 1]
    ]

    _CELL_WIDTH = 9
    _CELL_HEIGHT = 5

    @classmethod
    def create_grid_42pattern(
        cls,
        val_width: int,
        val_height: int
    ) -> tuple[
            list[list[int]],
            set[tuple[int, int]]
    ]:
        width: int = (2 * val_width) + 1
        height: int = (2 * val_height) + 1

        if width <= 0:
            raise Pattern42Error(f"Invalid width {width}")
        if height <= 0:
            raise Pattern42Error(f"Invalid height {height}")

        if width < cls._CELL_WIDTH or height < cls._CELL_HEIGHT:
            raise Pattern42Error("Size to small for 42 pattern")

        grid: list[list[int]] = [
            [1 for _ in range(width)]
            for _ in range(height)
        ]
        positions: set[tuple[int, int]] = set()

        offset_x = (val_width - cls._CELL_WIDTH) // 2
        offset_y = (val_height - cls._CELL_HEIGHT) // 2

        for row in range(5):
            for col in range(4):
                if cls._DIGIT_4[row][col] == 1:
                    gx = (offset_x + col) * 2 + 1
                    gy = (offset_y + row) * 2 + 1
                    grid[gy][gx] = 2
                    positions.add((gx, gy))

                if cls._DIGIT_2[row][col] == 1:
                    gx = (offset_x + col + 4) * 2 + 1
                    gy = (offset_y + row) * 2 + 1
                    grid[gy][gx] = 2
                    positions.add((gx, gy))

        return (grid, positions)

    @classmethod
    def is_42_position(
        cls,
        points: tuple[int, int],
        width: int, height: int
    ) -> bool:
        _, positions = Pattern42.create_grid_42pattern(width, height)
        val: tuple[int, int] = (2 * points[0] + 1, 2 * points[1] + 1)
        if val in positions:
            return True

        return False
