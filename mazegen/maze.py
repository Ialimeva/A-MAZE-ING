from typing import Optional


class MazeError(Exception):
    pass


class Maze:
    def __init__(
        self,
        grid: Optional[list[list[int]]] = None,
        entry_point: Optional[tuple[int, int]] = None,
        exit_point: Optional[tuple[int, int]] = None
    ) -> None:
        self.__grid: list[list[int]] = grid or []
        self.__entry: Optional[tuple[int, int]] = entry_point
        self.__exit: Optional[tuple[int, int]] = exit_point

        if entry_point:
            self.__entry = entry_point
        if exit_point:
            self.__exit = exit_point

    @property
    def width(self) -> int:
        return (len(self.__grid[0]) if self.__grid else 0)

    @property
    def height(self) -> int:
        return (len(self.__grid) if self.__grid else 0)

    @property
    def grid(self) -> list[list[int]]:
        return self.__grid

    @property
    def grid_hex(self) -> list[list[str]]:
        return self.__parsing_hex()

    @property
    def entry(self) -> tuple[int, int]:
        if self.__entry is None:
            raise MazeError("No Entry point given")
        return (2 * self.__entry[0] + 1, 2 * self.__entry[1] + 1)

    @property
    def exit(self) -> tuple[int, int]:
        if self.__exit is None:
            raise MazeError("No Exit point given")
        return (2 * self.__exit[0] + 1, 2 * self.__exit[1] + 1)

    def __parsing_hex(self) -> list[list[str]]:
        if not self.__grid:
            raise MazeError("Empty grid")
        output: list[list[str]] = []
        height: int = len(self.__grid)
        width: int = len(self.__grid[0])

        for i in range(1, height - 1, 2):
            row: list[str] = []
            for j in range(1, width - 1, 2):
                west = self.__grid[i][j - 1]
                south = self.__grid[i + 1][j]
                east = self.__grid[i][j + 1]
                north = self.__grid[i - 1][j]

                value = (
                    (north << 0) |
                    (east << 1) |
                    (south << 2) |
                    (west << 3)
                )

                row += [format(value, "X")]
            output += [row]

        return output

    def set_grid(self, grid: list[list[int]]) -> None:
        self.__grid = grid

    def set_entry(self, entry_point: tuple[int, int]) -> None:
        self.__entry = entry_point

    def set_exit(self, exit_point: tuple[int, int]) -> None:
        self.__exit = exit_point
