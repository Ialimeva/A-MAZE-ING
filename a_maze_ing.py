#!/usr/bin/env python3

from core import ConfigManager, MazeExporter, Pattern42
from mazegen import MazeGenerator
from cli_render import Render
from typing import Optional


def main() -> None:
    config_manager: ConfigManager = ConfigManager("config.txt")
    configs: dict[
        str,
        int | tuple[int, int] | str | bool | Optional[int]
    ] = config_manager.get_config()

    exporter: MazeExporter = MazeExporter(
        configs["output_file"],
        configs["entry"],
        configs["exit"]
    )

    maze_generator: MazeGenerator = MazeGenerator(
        configs["width"],
        configs["height"],
        configs["perfect"],
        grid=Pattern42.create_grid_42pattern(
            configs["width"],
            configs["height"],
        )
    )

    render: Render = Render()

    gen = maze_generator.generate_step()
    final_grid: list[list[int]] = []

    for g in gen:
        final_grid = g
        render.set_grid(final_grid)
        render.render_grid()

    render.set_grid(final_grid)
    render.render_grid()

    exporter.set_grid(final_grid)
    exporter.export_maze()


if __name__ == "__main__":
    main()
