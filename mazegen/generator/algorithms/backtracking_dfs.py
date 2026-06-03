"""
    Algorithm Generator, backtracking approach
    DFS (Depth-first search)

    This algo is a graph/tree algorithm that explores
    as far as possible while the position is valid, and
    backtrack on invalid position
"""

from ..generator_base import MazeGenerator
from typing import Generator
from ...maze import Maze
from ...maze_config import MazeConfig


class GeneratorDFS(MazeGenerator):
    """
        Representation of the DFS Algorithm

        Class Attributes:
            algorithm_name = "dfs", for register
    """
    algorithm_name = "dfs"

    def __init__(
        self,
        configs: MazeConfig,
    ) -> None:
        """
            Contructor, initialization of the instance

            Attributes:
                self.__visited (set[tuple[int, int]]):
                    containt visited position
        """
        super().__init__(configs)
        self.__visited: set[tuple[int, int]] = set()

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

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.__visited.add((start_x, start_y))
        self._maze.set_path(start_x, start_y)

        while stack:
            pos_x, pos_y = stack[-1]

            directions: list[tuple[int, int]] = [
                (2, 0),
                (-2, 0),
                (0, -2),
                (0, 2)
            ]
            self._random.shuffle(directions)

            pushed: bool = False
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y

                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    self.__visited.add((npos_x, npos_y))
                    stack.append((npos_x, npos_y))

                    self._maze.set_path((dx // 2) + pos_x, (dy // 2) + pos_y)
                    self._maze.set_path(npos_x, npos_y)

                    yield self._maze

                    pushed = True
                    break

            if not pushed:
                stack.pop()

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
