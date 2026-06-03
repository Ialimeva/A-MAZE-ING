"""
    Algorithm Generator, Prim's approch

    This algo is greedy algorithm used to
    find the MST (Minimum Spanning Tree) of
    a connected, weighted, undirected graph
"""

from ..generator_base import MazeGenerator
from typing import Generator
from ...maze import Maze
from ...maze_config import MazeConfig


class GeneratorPrims(MazeGenerator):
    """
        Representation of the Prim's Algorithm

        Class Attributes:
            algorithm_name = "prims", for register
    """
    algorithm_name = "prims"

    def __init__(self, configs: MazeConfig) -> None:
        """
            Contructor, initialization of the instance

            Attributes:
                self.__visited (set[tuple[int, int]]):
                    containt visited position
        """
        super().__init__(configs)
        self.__visited: set[tuple[int, int]] = set()

    def __get_neighbors(self, x: int, y: int) -> list[
        tuple[
            int,
            int,
            int,
            int
        ]
    ]:
        """
            Return all unvisited neighboring cells of a position

            Args:
                x, y (int): Position to evaluate

            Return:
                list[tuple[int, int, int, int]]: position of the cell
                                                + neighbors
        """
        edges: list[tuple[int, int, int, int]] = []
        directions: list[tuple[int, int]] = [
            (2, 0),
            (-2, 0),
            (0, -2),
            (0, 2)
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                self.is_valid_pos(nx, ny) and
                (nx, ny) not in self.__visited
            ):
                edges.append((x, y, nx, ny))

        return edges

    def __carve(
        self,
        start_x: int,
        start_y: int
    ) -> Generator[Maze, None, None]:
        """
            The heart of the algorithm

            Agrs:
                start_x, start_y (int): starting position

            Return:
                Generator[Maze, None, None]: yield position visited
        """
        self.__visited.clear()

        self.__visited.add((start_x, start_y))
        self._maze.set_path(start_x, start_y)

        frontiers: list[tuple[
            int,
            int,
            int,
            int]
        ] = self.__get_neighbors(start_x, start_y)

        while frontiers:
            idx = self._random.randrange(len(frontiers))
            frontiers[idx], frontiers[-1] = frontiers[-1], frontiers[idx]
            cx, cy, nx, ny = frontiers.pop()

            if (nx, ny) not in self.__visited:
                wall_x = (cx + nx) // 2
                wall_y = (cy + ny) // 2

                self._maze.set_path(wall_x, wall_y)
                self._maze.set_path(nx, ny)

                self.__visited.add((nx, ny))
                frontiers.extend(self.__get_neighbors(nx, ny))

                yield self._maze

        yield self._maze

    def generate(self) -> Maze:
        """
            Generate the Maze at once

            Return:
                Maze: the full maze
        """
        self.__visited.clear()
        gen = self.__carve(1, 1)

        for _ in gen:
            pass
        return super().generate()

    def generate_step(self) -> Generator[Maze, None, None]:
        """
            Generate the Maze step by step

            Return:
                yield carve position in the maze
                Maze: the full maze
        """
        self.__visited.clear()
        gen = self.__carve(1, 1)

        yield self._maze
        yield from gen
        yield from super().generate_step()
