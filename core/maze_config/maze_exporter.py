from typing import Optional


class MazeExporterError(Exception):
    pass


class MazeExporter:
    def __init__(
        self,
        filename: str,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        grid: Optional[list[list[int]]] = None,
    ) -> None:
        if not filename:
            raise MazeExporterError("Invalid file")

        self.__file: str = filename
        self.__grid: list[list[int]] = []
        if grid:
            self.__grid = grid

        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_

    def set_grid(self, grid: list[list[int]]) -> None:
        if not grid:
            raise MazeExporterError("Invalid Grid")
        self.__grid = grid

    def export_maze(self) -> None:
        try:
            with open(self.__file, "w") as f:
                output: str = self.__parse_grid()
                f.write(output)

                f.write("\n")
                f.write(str(self.entry[0]) + "," + str(self.entry[1]) + "\n")
                f.write(str(self.exit[0]) + "," + str(self.exit[1]) + "\n")

        except Exception as e:
            raise MazeExporterError(f"Export failed: {e}")

    def __parse_grid(self) -> str:
        if not self.__grid:
            raise MazeExporterError("Empty grid")
        output: str = ""
        height: int = len(self.__grid)
        width: int = len(self.__grid[0])

        for i in range(1, height - 1, 2):
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

                output += format(value, "X")
            output += "\n"

        return output
