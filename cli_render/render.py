class Render:
    def __init__(self) -> None:
        self._grid: list[list[int]] = []

    def set_grid(self, grid: list[list[int]]) -> None:
        self._grid = grid

    def render_grid(self) -> None:
        output: str = ""
        for row in self._grid:
            for cell in row:
                if (cell % 2) == 0:
                    output += " "
                else:
                    output += "█"
            output += "\n"

        print(output)

