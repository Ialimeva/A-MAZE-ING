"""
    Base of All implemented generator algorithm
"""

from typing import Generator
from abc import ABC, abstractmethod
from ..maze import Maze
from ..maze_config import MazeConfig
from ..maze_register import GeneratorRegistry
import random


class GeneratorError(Exception):
    """
        Error Raise on Generator
    """
    pass


class MazeGenerator(ABC):
    """
        Represent the base class of all implemented generator algorithm
        Only child class can be used for generator

        Class Attributes:
            algorithm_name (str): Default to None, given when need to Register
            _chance (float): used for imperfect maze

        Attributes:
            width, height (int)
            grid (list[list[int]]): Represent the maze grid
            entry, exit (tuple[int, int]): Point of the entry and exit
    """

    algorithm_name: str | None = None
    _chance: float = 0.05

    def __init__(
        self,
        configs: MazeConfig,
    ) -> None:
        """
            Constructor, initialization of the instance

            Args:
                configs(MazeConfig): Configuration of the maze
        """
        self.__width: int = 2 * configs.width + 1
        self.__height: int = 2 * configs.height + 1
        self._grid: list[list[int]] = (
            configs.grid if configs.grid is not None
            else MazeGenerator.initiate_grid(configs.width, configs.height)
        )

        self.entry: tuple[int, int] = configs.entry_point
        self.exit: tuple[int, int] = configs.exit_point
        self._maze: Maze = Maze(
            grid=self._grid,
            entry_point=self.entry,
            exit_point=self.exit
        )

        self._perfect: bool = configs.perfect
        self._random: random.Random = random.Random(configs.seed)

    def __init_subclass__(cls) -> None:
        """
            Initialization of subclass

            Register the subclass only when given a name
        """
        super().__init_subclass__()

        if cls.algorithm_name is not None:
            GeneratorRegistry.register(
                cls.algorithm_name,
                cls
            )

    @abstractmethod
    def generate(self) -> Maze:
        """
            Method to generate full maze at once
        """
        if not self._perfect:
            self._add_loop()
        return self._maze

    @abstractmethod
    def generate_step(self) -> Generator[Maze, None, None]:
        """
            Method to generate maze step by step
        """
        if not self._perfect:
            yield from self._add_loop_step()
        yield self._maze

    def is_valid_pos(self, x: int, y: int) -> bool:
        """
            Evaluation of valid and invalid position on the grid

            Args:
                x, y (int): Coordinate of the position

            Return:
                bool: State of the validity
        """
        return (
            0 < x < self.__width and
            0 < y < self.__height and
            self._maze.get_value(x, y) != 2
        )

    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        """
            Initialization of grid

            Args:
                width, height (int): configuration of the grid

            Return:
                list[list[int]]: grid initialized
        """
        return [
            [1 for _ in range(2 * width + 1)]
            for _ in range(2 * height + 1)
        ]

    def _compute_protected(self) -> set[tuple[int, int]]:
        """
            Getter of all constant positions in the grid

            Return:
                set[tuple[int, int]]: all constant, static position on the grid
        """

        protected: set[tuple[int, int]] = set()

        for y in range(1, self.__height, 2):
            for x in range(1, self.__width, 2):
                if self._maze.get_value(x, y) == 2:

                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            nx, ny = dx + x, dy + y

                            if (
                                0 <= nx < self.__width and
                                0 <= ny < self.__height
                            ):
                                protected.add((nx, ny))

        return protected

    def __loop_core(
        self,
        protected: set[tuple[int, int]]
    ) -> Generator[tuple[int, int], None, None]:
        """
            Carve on the already generated maze if imperfect maze

            Args:
                protected (set[tuple[int, int]]): position of constant position

            Return:
                Generator[tuple[int, int]]: yield of position carve
        """

        grid: list[list[int]] = self._maze.grid

        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):

                if (
                    grid[y][x] != 2 and
                    (x % 2 != 0 or y % 2 != 0) and
                    (x, y) not in protected
                ):

                    h_connection: bool = (
                        grid[y][x - 1] == 0 and
                        grid[y][x + 1] == 0
                    )
                    v_connection: bool = (
                        grid[y - 1][x] == 0 and
                        grid[y + 1][x] == 0
                    )

                    if (
                        (h_connection or v_connection) and
                        self._random.random() < MazeGenerator._chance
                    ):
                        yield (x, y)

    def _add_loop(self) -> None:
        """
            Addition of carve in the grid at once.
        """
        protected: set[tuple[int, int]] = self._compute_protected()
        for x, y in self.__loop_core(protected):
            self._maze.set_path(x, y)

    def _add_loop_step(self) -> Generator[Maze, None, None]:
        """
            Addition of carve in the grid step by step.
        """
        protected: set[tuple[int, int]] = self._compute_protected()

        for x, y in self.__loop_core(protected):
            self._maze.set_path(x, y)
            yield self._maze
