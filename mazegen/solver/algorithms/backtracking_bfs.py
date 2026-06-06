"""Breadth-first search maze solving algorithm."""

from ...solver.solver_base import MazeSolver
from typing import Deque, Generator, Optional
from collections import deque
from ...maze import Maze


class SolverBFS(MazeSolver):
    """Maze solving using breadth-first search."""

    algorithm_name = "bfs"

    def __init__(
        self,
        maze: Maze,
        seed: Optional[int] = None
    ) -> None:
        """Initialize BFS solver.

        Args:
            maze: Maze to solve.
            seed: Random seed.
        """
        super().__init__(maze, seed)
        self.__visited: set[tuple[int, int]] = set()
        self.__path: list[tuple[int, int]] = []

    def __reconstruct_path(
        self,
        parent: dict[tuple[int, int], tuple[int, int] | None]
    ) -> None:
        """Reconstruct the solution path.

        Args:
            parent: Mapping from each visited position to its parent.
        """
        path: list[tuple[int, int]] = []
        node: tuple[int, int] | None = self._maze.exit

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        self.__path = path

    def __find(
        self
    ) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        """Solve the maze using breadth-first search.

        Yields:
            Intermediate visited positions.

        Returns:
            Path from the entry point to the exit point.
        """
        queue: Deque[tuple[int, int]] = deque([self._maze.entry])
        parent: dict[tuple[int, int], tuple[int, int] | None] = {
            self._maze.entry: None
        }
        self.__visited.add(self._maze.entry)

        while queue:
            pos_x, pos_y = queue.popleft()
            yield (pos_x, pos_y)

            if (pos_x, pos_y) == self._maze.exit:
                self.__reconstruct_path(parent)
                return self.__path

            directions: list[tuple[int, int]] = [
                (0, -2),
                (2, 0),
                (0, 2),
                (-2, 0)
            ]
            self._random.shuffle(directions)

            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y
                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    mid_x: int = pos_x + dx // 2
                    mid_y: int = pos_y + dy // 2
                    if (self._maze.get_value(mid_x, mid_y) == 0):
                        self.__visited.add((npos_x, npos_y))
                        queue.append((npos_x, npos_y))
                        parent[(npos_x, npos_y)] = (pos_x, pos_y)

        return self.__path

    def solve(self) -> list[tuple[int, int]]:
        """Solve the maze completely.

        Returns:
            Path from the entry point to the exit point.
        """
        self.__visited.clear()
        gen = self.__find()

        while True:
            try:
                next(gen)
            except StopIteration as e:
                self.__path = e.value if e.value else []
                break

        return (self.__path)

    def solve_step(
        self
    ) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        """Solve the maze incrementally.

        Yields:
            Intermediate visited positions.

        Returns:
            Path from the entry point to the exit point.
        """
        self.__visited.clear()
        gen = self.__find()
        return (yield from gen)
