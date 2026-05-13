from typing import Generator
from abc import ABC, abstractmethod
from mazegen.maze import Maze
from mazegen.maze_config import MazeConfig
from mazegen.maze_register import GeneratorRegistry
import random


class GeneratorError(Exception):
    pass


class MazeGenerator(ABC):

    algorithm_name: str | None = None
    _chance: float = 0.05

    def __init__(
        self,
        configs: MazeConfig,
    ) -> None:
        self.__width: int = 2 * configs.width + 1
        self.__height: int = 2 * configs.height + 1
        self._grid: list[list[int]] = (
            configs.grid if configs.grid is not None
            else MazeGenerator.initiate_grid(self.__width, self.__height)
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
        super().__init_subclass__()

        if cls.algorithm_name is not None:
            GeneratorRegistry.register(
                cls.algorithm_name,
                cls
            )

    @abstractmethod
    def generate(self) -> Maze:
        if not self._perfect:
            self._add_loop()
        return self._maze

    @abstractmethod
    def generate_step(self) -> Generator[Maze, None, None]:
        if not self._perfect:
            yield from self._add_loop_step()
        yield self._maze

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self.__width and
            0 < y < self.__height and
            self._maze.grid[y][x] != 2
        )

    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        return [
            [1 for _ in range(2 * width + 1)]
            for _ in range(2 * height + 1)
        ]

    def _compute_protected(self) -> set[tuple[int, int]]:
        protected: set[tuple[int, int]] = set()

        for y in range(1, self.__height, 2):
            for x in range(1, self.__width, 2):
                if self._maze.grid[y][x] == 2:

                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            nx, ny = dx + x, dy + y

                            if (
                                0 <= nx < self.__width and
                                0 <= ny < self.__height
                            ):
                                protected.add((nx, ny))

        return protected

    def _add_loop(self) -> None:
        protected: set[tuple[int, int]] = self._compute_protected()

        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):

                if (
                    self._maze.grid[y][x] != 2 and
                    self._maze.grid[y][x] == 1 and
                    (x % 2 != 0 or y % 2 != 0) and
                    (x, y) not in protected
                ):

                    h_connection: bool = (
                        self._maze.grid[y][x - 1] == 0 and
                        self._maze.grid[y][x + 1] == 0
                    )
                    v_connection: bool = (
                        self._maze.grid[y - 1][x] == 0 and
                        self._maze.grid[y + 1][x] == 0
                    )

                    if (
                        (h_connection or v_connection) and
                        self._random.random() < MazeGenerator._chance
                    ):
                        self._maze.grid[y][x] = 0

    def _add_loop_step(self) -> Generator[Maze, None, None]:
        protected: set[tuple[int, int]] = self._compute_protected()

        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):

                if (
                    self._maze.grid[y][x] != 2 and
                    self._maze.grid[y][x] == 1 and
                    (x % 2 != 0 or y % 2 != 0) and
                    (x, y) not in protected
                ):

                    h_connection: bool = (
                        self._maze.grid[y][x - 1] == 0 and
                        self._maze.grid[y][x + 1] == 0
                    )
                    v_connection: bool = (
                        self._maze.grid[y - 1][x] == 0 and
                        self._maze.grid[y + 1][x] == 0
                    )

                    if (
                        (h_connection or v_connection) and
                        self._random.random() < MazeGenerator._chance
                    ):
                        self._maze.grid[y][x] = 0
                        yield self._maze
