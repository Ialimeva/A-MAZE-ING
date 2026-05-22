from .render import Render
from typing import Any
from mazegen import Maze
from core import MazeManager
from enum import Enum
import time


class VisualTermError(Exception):
    pass


class Color(Enum):
    reset = "\033[0m"
    green = "\033[032m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"


a_maze_ing: str = (r"""
 █████╗       ███╗   ███╗ █████╗ ███████╗███████╗      ██╗███╗   ██╗ ██████╗
██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝      ██║████╗  ██║██╔════╝
███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  █████╗██║██╔██╗ ██║██║  ███╗
██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ╚════╝██║██║╚██╗██║██║   ██║
██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗      ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝  ╚═══╝ ╚═════╝
""")


class VisualTerm:
    def __init__(self, config: dict[str, Any]) -> None:
        self.__render: Render = Render()
        self.__config: dict[str, Any] = config
        self.__maze: Maze = Maze()
        self.__path_visited: list[tuple[int, int]] = []
        self.__path_solution: list[tuple[int, int]] = []

        self.__is_solve = False
        self.__is_running = True
        self.__is_maze_generate = False
        self.__path_show = True

        self.__menu: str = VisualTerm.get_menu()
        VisualTerm.introduction()

    @staticmethod
    def introduction():
        output: list[str] = a_maze_ing.split("\n")
        for line in output:
            print(line)
            time.sleep(0.25)
        print("Loading ...")
        time.sleep(2)

    def __render_maze(self) -> None:
        if not self.__is_maze_generate:
            gen = MazeManager.generate_step(self.__config)
            for maze in gen:
                self.__maze = maze
                self.__render.render_maze(self.__maze)
            self.__is_maze_generate = True
        else:
            self.__render.render_maze(self.__maze)

    def __solve_maze(self) -> None:
        gen = MazeManager.solve_step(self.__maze, self.__config)
        for path in gen:
            if path.visited is not None:
                self.__path_visited.append(path.visited)
            if path.solution is not None:
                self.__path_solution = path.solution

            self.__render.render_maze(self.__maze, self.__path_visited)
        self.__is_solve = True

    def __render_path(self) -> None:
        if not self.__is_solve:
            self.__solve_maze()
        expand = self.__render.expand_path(self.__path_solution)
        self.__render.render_maze(self.__maze, expand)

    def __manage_input(self) -> None:
        print(self.__menu)
        val = input("Your choice: ")

        if val == "g":
            self.__is_maze_generate = False
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
            if self.__path_show:
                self.__render.render_maze(self.__maze)
                self.__path_show = False
            else:
                self.__render_path()
                self.__path_show = True

        else:
            pass

    def run(self) -> None:
        while self.__is_running:
            self.__manage_input()

    @staticmethod
    def get_menu() -> str:
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
