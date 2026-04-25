import time
from enum import Enum


class Brick(Enum):
    WALL = "█"
    PATH = " "
    FT = "\033[33m▓\033[0m"
    POINT = "\033[34m█\033[0m"


class Render:
    clear = "\033[H\033[J"

    def __init__(self) -> None:
        self._grid: list[list[int]] = []

    def set_grid(self, grid: list[list[int]]) -> None:
        self._grid = grid

    def set_point(self, entry: tuple[int, int], exit_: tuple[int, int]) -> None:
        self._entry: tuple[int, int] = (2 * entry[0] + 1, 2 * entry[1] + 1)
        self._exit: tuple[int, int] = (2 * exit_[0] + 1, 2 * exit_[1] + 1)

    def render_grid(self) -> None:
        output: str = Render.clear

        for y, row in enumerate(self._grid):
            for x, cell in enumerate(row):
                if (
                    (x, y) == self._entry or
                    (x, y) == self._exit
                ):
                    output += Brick.POINT.value
                elif cell == 2:
                    output += Brick.FT.value
                elif (cell % 2) == 0:
                    output += Brick.PATH.value
                else:
                    output += Brick.WALL.value
            output += "\n"

        time.sleep(0.02)
        print(output)
