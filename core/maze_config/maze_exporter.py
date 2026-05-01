from typing import Optional


class MazeExporterError(Exception):
    pass


class MazeExporter:

    @classmethod
    def export_maze_file(
        cls,
        filename: str,
        grid: list[list[int]],
        entry_point: Optional[tuple[int, int]],
        exit_point: Optional[tuple[int, int]]
    ) -> None:
        try:
            if not filename:
                raise MazeExporterError("Invalid file")
            with open(filename, "w") as f:
                res: list[list[str]] = cls.__parse_grid(grid)
                output: str = "\n".join("".join(row) for row in res)
                f.write(output)
                f.write("\n")

                if (entry_point and exit_point):
                    f.write("\n")
                    f.write(str(entry_point[0]) + "," + str(entry_point[1]) + "\n")
                    f.write(str(exit_point[0]) + "," + str(exit_point[1]) + "\n")

        except Exception as e:
            raise MazeExporterError(f"Export failed: {e}")

    @classmethod
    def export_maze(cls, grid: list[list[int]]) -> list[list[str]]:
        return cls.__parse_grid(grid)

    @classmethod
    def __parse_grid(cls, grid: list[list[int]]) -> list[list[str]]:
        if not grid:
            raise MazeExporterError("Empty grid")
        output: list[list[str]] = []
        height: int = len(grid)
        width: int = len(grid[0])

        for i in range(1, height - 1, 2):
            row: list[str] = []
            for j in range(1, width - 1, 2):
                west = grid[i][j - 1]
                south = grid[i + 1][j]
                east = grid[i][j + 1]
                north = grid[i - 1][j]

                value = (
                    (north << 0) |
                    (east << 1) |
                    (south << 2) |
                    (west << 3)
                )

                row += [format(value, "X")]
            output += [row]

        return output
