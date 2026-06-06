"""Wilson's algorithm for maze generation."""

from ..generator_base import MazeGenerator
from typing import Generator
from ...maze import Maze
from ...maze_config import MazeConfig


class GeneratorWilsons(MazeGenerator):
    """Maze generation using Wilson's algorithm (loop-erased random walks)."""
    
    algorithm_name = "wilsons"

    def __init__(self, configs: MazeConfig) -> None:
        """Initialize Wilson's generator.

        Args:
            configs: Maze configuration.
        """
        super().__init__(configs)
        self.__visited: set[tuple[int, int]] = set()

    def __get_all_cell(self) -> list[tuple[int, int]]:
        """Get all valid maze cells.

        Returns:
            List of cell coordinates.
        """
        return ([
            (x, y) for x in range(1, self._maze.width, 2)
            for y in range(1, self._maze.height, 2)
            if self.is_valid_pos(x, y)
        ])

    def __get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Get neighboring cells.

        Args:
            x: X coordinate.
            y: Y coordinate.

        Returns:
            List of neighbor coordinates.
        """
        edges: list[tuple[int, int]] = []
        directions: list[tuple[int, int]] = [
            (2, 0),
            (-2, 0),
            (0, -2),
            (0, 2)
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_pos(nx, ny):
                edges.append((nx, ny))

        return edges

    def __carve(
        self,
        start_x: int,
        start_y: int
    ) -> Generator[Maze, None, None]:
        """Carve passages using loop-erased random walks.

        Args:
            cells: List of cells to process.

        Yields:
            Intermediate maze states.
        """
        self.__visited.clear()

        all_cells: list[tuple[int, int]] = self.__get_all_cell()
        root: tuple[int, int] = (start_x, start_y)
        self.__visited.add(root)

        while len(self.__visited) < len(all_cells):
            unvisited: list[tuple[int, int]] = [
                c for c in all_cells if (c not in self.__visited and
                                         self.is_valid_pos(*c))
            ]
            starting_cell: tuple[int, int] = self._random.choice(unvisited)
            current: tuple[int, int] = starting_cell

            path_directions: dict[tuple[int, int], tuple[int, int]] = {}

            while current not in self.__visited:
                neighbors: list[tuple[
                    int,
                    int]
                ] = self.__get_neighbors(*current)
                next_cell: tuple[int, int] = self._random.choice(neighbors)

                path_directions[current] = next_cell
                current = next_cell

            carve_ptr: tuple[int, int] = starting_cell
            while carve_ptr != current:
                next_cell = path_directions[carve_ptr]

                wall_x = (carve_ptr[0] + next_cell[0]) // 2
                wall_y = (carve_ptr[1] + next_cell[1]) // 2

                self._maze.set_path(carve_ptr[0], carve_ptr[1])
                self._maze.set_path(wall_x, wall_y)
                self._maze.set_path(next_cell[0], next_cell[1])

                self.__visited.add(carve_ptr)

                carve_ptr = next_cell
                yield self._maze

            self.__visited.add(current)
            yield self._maze

    def generate(self) -> Maze:
        """Generate the complete maze.

        Returns:
            Generated Maze instance.
        """
        self.__visited.clear()
        gen = self.__carve(1, 1)

        for _ in gen:
            pass
        return super().generate()

    def generate_step(self) -> Generator[Maze, None, None]:
        """Generate maze incrementally.

        Yields:
            Intermediate maze states.
        """
        self.__visited.clear()
        gen = self.__carve(1, 1)

        yield self._maze
        yield from gen
        yield from super().generate_step()
