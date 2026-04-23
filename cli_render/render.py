import time


class Render:
    clear = "\033[H\033[J"

    def __init__(self) -> None:
        self._grid: list[list[int]] = []

    def set_grid(self, grid: list[list[int]]) -> None:
        self._grid = grid

    def render_grid(self) -> None:
        output: str = Render.clear
        for row in self._grid:
            for cell in row:
                if cell == 2:
                    output += "\033[33m▓\033[0m"
                elif (cell % 2) == 0:
                    output += " "
                else:
                    output += "█"
            output += "\n"

        time.sleep(0.02)
        print(output)
