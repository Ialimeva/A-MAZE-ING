"""Render mazes in the terminal using ANSI colors.

This module provides utilities for coloring and displaying mazes
and their solution paths in a terminal.
"""


import time
from enum import Enum
from mazegen import Maze
from typing import Optional
import random


class ColorPalette(Enum):
    """Define ANSI escape sequences used for terminal colors."""

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
    """Manage predefined color palettes for terminal rendering."""

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
        """Select a color palette.

        Returns:
            A dictionary mapping rendering elements to ANSI colors.
        """
        return random.choice(cls.PALETTES)


class Brick:
    """Represent the visual symbols used to render a maze."""

    def __init__(self) -> None:
        """Initialize the rendering symbols with a random color palette."""
        self.palette: dict[str, str] = {}
        self.change_color()
        self.update()

    def change_color(self) -> None:
        """Switch to a new color palette."""
        tmp: dict[str, str] = Palette.get_color()
        while (tmp == self.palette):
            tmp = Palette.get_color()
        self.palette = tmp
        self.update()

    def update(self) -> None:
        """Update the rendered symbols according to the current palette."""
        self.wall: str = self.palette["path"] + "  " + ColorPalette.RESET.value
        self.path: str = self.palette["wall"] + "██" + ColorPalette.RESET.value
        self.res: str = self.palette["res"] + "▓▓" + ColorPalette.RESET.value
        self.ft: str = self.palette["ft"] + "▓▓" + ColorPalette.RESET.value
        self.point: str = (
            self.palette["point"] + "██" + ColorPalette.RESET.value
        )


class Render:
    """Render mazes and solution paths in the terminal."""

    clear = "\033[H\033[J"

    def __init__(self) -> None:
        """Initialize the renderer."""
        self.__brick = Brick()

    def render_maze(
        self,
        maze: Maze,
        path: Optional[list[tuple[int, int]]] = None
    ) -> None:
        """Display a maze in the terminal.

        Optionally highlights the solution path, entry point,
        exit point, and the 42 pattern.

        Args:
            maze: Maze to render.
            path: Optional path to highlight.

        Raises:
            ValueError: If the maze grid is empty.
        """
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
        """Expand a cell path to include intermediate wall positions.

        Args:
            path: Sequence of maze positions.

        Returns:
            A path containing both cells and the walls connecting
            consecutive positions.
        """
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
        """Change the current rendering palette."""
        self.__brick.change_color()
