from enum import Enum
from mazegen import Maze
from typing import Optional


class Brick(Enum):
    WALL = "█"
    PATH = " "
    RES = "\033[32m▓\033[0m"
    FT = "\033[33m▓\033[0m"
    POINT = "\033[34m█\033[0m"


class Render:
    clear = "\033[H\033[J"

    def render_maze(
        self,
        maze: Maze,
        path: Optional[list[tuple[int, int]]] = None
    ) -> None:
        output: str = Render.clear

        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                if path is not None and (x, y) in path:
                    output += Brick.RES.value
                    continue
                if (
                    (x, y) == maze.entry or
                    (x, y) == maze.exit
                ):
                    output += Brick.POINT.value
                elif cell == 2:
                    output += Brick.FT.value
                elif (cell % 2) == 0:
                    output += Brick.PATH.value
                else:
                    output += Brick.WALL.value

            output += "\n"

        # time.sleep(0.01)
        print(output)

    def _expand_path(
        self,
        path: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        full_path: list[tuple[int, int]] = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            full_path.append((x1, y1))
            full_path.append((x2, y2))

            # add the wall between them
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            full_path.append((mid_x, mid_y))

        return full_path
