from typing import Optional


class MazeExporterError(Exception):
    pass


class MazeExporter:
    def __init__(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        grid: Optional[list[list[int]]] = None,
    ) -> None:

        self.__grid: list[list[int]] = []
        if grid:
            self.__grid = grid

        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_

    def set_grid(self, grid: list[list[int]]) -> None:
        if not grid:
            raise MazeExporterError("Invalid Grid")
        self.__grid = grid

    def export_maze_file(self, filename: str) -> None:
        try:
            if not filename:
                raise MazeExporterError("Invalid file")
            with open(filename, "w") as f:
                res: list[list[str]] = self.__parse_grid()
                output: str = "\n".join("".join(row) for row in res)
                f.write(output)

                f.write("\n")
                f.write(str(self.entry[0]) + "," + str(self.entry[1]) + "\n")
                f.write(str(self.exit[0]) + "," + str(self.exit[1]) + "\n")

        except Exception as e:
            raise MazeExporterError(f"Export failed: {e}")

    def export_maze(self) -> list[list[str]]:
        return self.__parse_grid()

    def __parse_grid(self) -> list[list[str]]:
        if not self.__grid:
            raise MazeExporterError("Empty grid")
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
