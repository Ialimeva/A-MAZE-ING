from ..generator_base import MazeGenerator
from typing import Generator
from ...maze import Maze
from ...maze_config import MazeConfig


class GeneratorPrims(MazeGenerator):
    algorithm_name = "prims"

    def __init__(self, configs: MazeConfig) -> None:
        super().__init__(configs)
        self.__visited: set[tuple[int, int]] = set()

    def __get_neighbors(self, x, y) -> list[tuple[int, int, int, int]]:
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

    def __carve(self, start_x, start_y) -> Generator[Maze, None, None]:
        self.__visited.clear()

        self.__visited.add((start_x, start_y))
        self._maze.grid[start_y][start_x] = 0

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

                self._maze.grid[wall_y][wall_x] = 0
                self._maze.grid[ny][nx] = 0

                self.__visited.add((nx, ny))
                frontiers.extend(self.__get_neighbors(nx, ny))

                yield self._maze

        yield self._maze

    def generate(self) -> Maze:
        self.__visited.clear()
        gen = self.__carve(1, 1)

        for val in gen:
            self._maze = val
        return super().generate()

    def generate_step(self) -> Generator[Maze, None, None]:
        self.__visited.clear()
        gen = self.__carve(1, 1)

        yield self._maze
        yield from gen
        yield from super().generate_step()
