"""A* maze solving algorithm."""

from ..solver_base import MazeSolver
from typing import Generator, Optional
from ...maze import Maze
import heapq


class SolverAStar(MazeSolver):
    """Maze solving using the A* algorithm."""
    algorithm_name = "astar"

    def __init__(
        self,
        maze: Maze,
        seed: Optional[int] = None
    ) -> None:
        """Initialize A* solver.

        Args:
            maze: Maze to solve.
            seed: Random seed.
        """
        super().__init__(maze, seed)
        self.__visited: set[tuple[int, int]] = set()
        self.__path: list[tuple[int, int]] = []

    def __reconstruct_path(
        self,
        previous: dict[tuple[int, int], tuple[int, int]],
    ) -> None:
        """Reconstruct the solution path.

        Args:
            previous: Mapping from each visited position to its
                predecessor.
        """
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = self._maze.exit

        while current and current != self._maze.entry:
            if current not in previous:
                return None

            path.append(current)
            current = previous[current]

        path.append(self._maze.entry)
        path.reverse()
        self.__path = path

    def __manhattan_heuristic(
        self,
        val1: tuple[int, int],
        val2: tuple[int, int]
    ) -> int:
        """Compute the Manhattan distance between two positions.

        Args:
            val1: First position.
            val2: Second position.

        Returns:
            Manhattan distance between the two positions.
        """
        return (abs(val1[0] - val2[0]) + abs(val1[1] - val2[1]))

    def __find(
        self
    ) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        """Solve the maze using the A* algorithm.

        Yields:
            Intermediate visited positions.

        Returns:
            Path from the entry point to the exit point.
        """
        distances: dict[tuple[int, int], int] = {
            self._maze.entry: 0
        }
        priority_queue: list[
            tuple[int, tuple[int, int]]
        ] = [(0, self._maze.entry)]
        previous: dict[tuple[int, int], tuple[int, int]] = {}
        directions: list[tuple[int, int]] = [
            (0, -2),
            (2, 0),
            (0, 2),
            (-2, 0)
        ]

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)
            current_distance = distances[current_node]

            if current_node in self.__visited:
                continue

            self.__visited.add(current_node)

            if current_node == self._maze.exit:
                break

            yield current_node

            pos_x, pos_y = current_node
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y
                neighbor: tuple[int, int] = (npos_x, npos_y)

                if (
                    self.is_valid_pos(*neighbor) and
                    neighbor not in self.__visited
                ):
                    mid_x: int = pos_x + dx // 2
                    mid_y: int = pos_y + dy // 2
                    if (self._maze.get_value(mid_x, mid_y) == 0):
                        new_dist: int = current_distance + 1

                        if (
                            neighbor not in distances or
                            new_dist < distances[neighbor]
                        ):
                            distances[neighbor] = new_dist
                            priority = (
                                new_dist +
                                self.__manhattan_heuristic(
                                    neighbor,
                                    self._maze.exit
                                )
                            )
                            previous[neighbor] = current_node

                            heapq.heappush(
                                priority_queue,
                                (priority, neighbor)
                            )

        self.__reconstruct_path(previous)
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
