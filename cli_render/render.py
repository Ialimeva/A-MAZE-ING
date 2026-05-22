import time
from enum import Enum
from mazegen import Maze
from typing import Optional
import random


class ColorPalette(Enum):
    RESET = "\033[0m"

    # Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Backgrounds
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"


class Palette:
    PALETTES = [
        {
            "wall": ColorPalette.BRIGHT_BLUE.value,
            "path": ColorPalette.BLACK.value,
            "res": ColorPalette.BRIGHT_GREEN.value,
            "ft": ColorPalette.BRIGHT_YELLOW.value,
            "point": ColorPalette.BRIGHT_RED.value,
        },

        {
            "wall": ColorPalette.MAGENTA.value,
            "path": ColorPalette.BLACK.value,
            "res": ColorPalette.CYAN.value,
            "ft": ColorPalette.YELLOW.value,
            "point": ColorPalette.RED.value,
        },

        {
            "wall": ColorPalette.WHITE.value,
            "path": ColorPalette.BLACK.value,
            "res": ColorPalette.GREEN.value,
            "ft": ColorPalette.BLUE.value,
            "point": ColorPalette.MAGENTA.value,
        },

        {
            "wall": ColorPalette.BRIGHT_CYAN.value,
            "path": ColorPalette.BLACK.value,
            "res": ColorPalette.BRIGHT_MAGENTA.value,
            "ft": ColorPalette.BRIGHT_YELLOW.value,
            "point": ColorPalette.BRIGHT_WHITE.value,
        },
    ]

    @classmethod
    def get_color(cls) -> dict[str, str]:
        return random.choice(cls.PALETTES)


class Brick:
    def __init__(self) -> None:
        self.palette: dict[str, str] = {}
        self.change_color()
        self.update()

    def change_color(self) -> None:
        self.palette = Palette.get_color()
        self.update()

    def update(self) -> None:
        self.wall: str = self.palette["path"] + "▓▓" + ColorPalette.RESET.value
        self.path: str = self.palette["wall"] + "██" + ColorPalette.RESET.value
        self.res: str = self.palette["res"] + "▓▓" + ColorPalette.RESET.value
        self.ft: str = self.palette["ft"] + "▓▓" + ColorPalette.RESET.value
        self.point: str = (
            self.palette["point"] + "██" + ColorPalette.RESET.value
        )


class Render:
    clear = "\033[H\033[J"

    def __init__(self) -> None:
        self.__brick = Brick()

    def render_maze(
        self,
        maze: Maze,
        path: Optional[list[tuple[int, int]]] = None
    ) -> None:
        if maze.grid is None or not maze.grid:
            raise ValueError("Maze grid empty")

        output: str = Render.clear

        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                if path is not None and (x, y) in path:
                    output += self.__brick.res
                    continue
                if (
                    (x, y) == maze.entry or
                    (x, y) == maze.exit
                ):
                    output += self.__brick.point
                elif cell == 2:
                    output += self.__brick.ft
                elif (cell % 2) == 0:
                    output += self.__brick.path
                else:
                    output += self.__brick.wall

            output += "\n"

        time.sleep(0.01)
        print(output)

    def expand_path(
        self,
        path: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        full_path: list[tuple[int, int]] = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            full_path.append((x1, y1))
            full_path.append((x2, y2))

            # add the wall between them
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            full_path.append((mid_x, mid_y))

        return full_path

    def change_color(self) -> None:
        self.__brick.change_color()
