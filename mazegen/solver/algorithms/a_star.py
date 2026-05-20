from ...solver.solver_base import MazeSolver
from ...maze import Maze
from typing import Generator, Optional


class SolverAStar(MazeSolver):
    algorithm_name = "astar"

    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        super().__init__(maze, seed)
        self.__visited: set[tuple[int, int]] = set()
        self.__path: list[tuple[int, int]] = []

        self.__directions: list[tuple[int, int]] = [
            (0, -2),
            (2, 0),
            (0, 2),
            (-2, 0)
        ]

    def __manhattan_heuristic(
        self,
        val1: tuple[int, int],
        val2: tuple[int, int]
    ) -> int:
        return (abs(val1[0] - val2[0]) + abs(val1[1] - val2[1]))

    def __get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        edges: list[tuple[int, int]] = []
        for dx, dy in self.__directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_pos(nx, ny):
                edges.append((nx, ny))

        return edges

    def __find(self) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        ...

    def solve(self) -> list[tuple[int, int]]:
        self.__visited.clear()
        gen = self.__find()

        for val in gen:
            self.__path.append(val)

        return self.__path

    def solve_step(self) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        self.__visited.clear()
        gen = self.__find()
        return (yield from gen)
