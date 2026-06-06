"""Provide an interactive terminal interface for maze visualization.

This module allows users to generate, solve, and display mazes
through a text-based menu.
"""

from .render import Render
from typing import Any
from mazegen import Maze
from core import MazeManager
from enum import Enum
import random


class VisualTermError(Exception):
    """Raise when an error occurs in the terminal visualization."""

    pass


class Color(Enum):
    """Define ANSI escape sequences used by the terminal menu."""

    reset = "\033[0m"
    green = "\033[032m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"


class VisualTerm:
    """Manage the interactive terminal visualization of mazes."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the terminal visualization.

        Args:
            config: Maze configuration parameters.
        """
        self.__render: Render = Render()
        self.__config: dict[str, Any] = config
        self.__maze: Maze = Maze()
        self.__path: list[tuple[int, int]] = []

        self.__is_solve = False
        self.__is_running = True
        self.__is_maze_generate = False
        self.__path_show = True

        self.__menu: str = VisualTerm.get_menu()
        self.__generate_maze()

    def __render_maze(self) -> None:
        """Render the current maze.

        Generates a new maze if none has been created yet.
        """
        if not self.__is_maze_generate:
            self.__generate_maze()
        self.__render.render_maze(self.__maze)

    def __generate_maze(self) -> None:
        """Generate and display a maze step by step."""
        if not self.__is_maze_generate:
            gen = MazeManager.generate_step(self.__config)
            for maze in gen:
                self.__maze = maze
                self.__render.render_maze(self.__maze)
            self.__is_maze_generate = True

    def __solve_maze(self) -> None:
        """Solve the current maze and animate the process.

        The final solution path is stored internally.
        """
        gen = MazeManager.solve_step(self.__maze, self.__config)
        try:
            while True:
                self.__path.append(next(gen))
                self.__render.render_maze(self.__maze, self.__path)
        except StopIteration as e:
            self.__path = e.value

        self.__is_solve = True

    def __render_path(self) -> None:
        """Display the solution path.

        Solves the maze first if no solution has been computed.
        """
        if not self.__is_solve:
            self.__solve_maze()
        expand = self.__render.expand_path(self.__path)
        self.__render.render_maze(self.__maze, expand)

    def __manage_input(self) -> None:
        """Process a user command from the interactive menu.

        Supported commands allow generating a maze, solving it,
        changing colors, toggling the solution path, and quitting.
        """
        print(self.__menu)
        val = input("Your choice: ")

        if val == "g":
            self.__is_maze_generate = False
            self.__is_solve = False
            self.__path = []
            self.__config["seed"] = random.randint(0, 10000)
            self.__render_maze()

        if val == "q":
            self.__is_running = False

        if val == "s":
            if not self.__is_maze_generate:
                self.__render_maze()
            self.__render_path()

        if val == "c":
            self.__render.change_color()
            if self.__is_solve:
                self.__render_path()
            else:
                self.__render_maze()

        if val == "p":
            if not self.__is_maze_generate:
                self.__generate_maze()
                self.__solve_maze()
            if self.__path_show:
                self.__render.render_maze(self.__maze)
                self.__path_show = False
            else:
                self.__render_path()
                self.__path_show = True

    def run(self) -> None:
        """Start the interactive terminal interface."""
        while self.__is_running:
            self.__manage_input()

    @staticmethod
    def get_menu() -> str:
        """Build the menu displayed to the user.

        Returns:
            A formatted string containing the available commands.
        """
        menu: str = ""
        menu += (
            Color.magenta.value +
            "=== A-Maze-ing Menu ===" +
            Color.reset.value + "\n"
        )
        menu += (
            Color.blue.value +
            "q) - " +
            Color.reset.value + "Quit" + "\n"
        )
        menu += (
            Color.blue.value +
            "g) - " +
            Color.reset.value +
            "Generate new maze" + "\n"
        )
        menu += (
            Color.blue.value +
            "s) - " +
            Color.reset.value +
            "Solve maze" +
            "\n"
        )
        menu += (
            Color.blue.value +
            "c) - " +
            Color.reset.value +
            "Change color" +
            "\n"
        )
        menu += (
            Color.blue.value +
            "p) - " +
            Color.reset.value +
            "Show path" +
            "\n"
        )
        return menu
