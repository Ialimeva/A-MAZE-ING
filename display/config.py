from typing import Any

maze_config: dict[str, Any] = {
    "colums": 0,
    "rows": 0,
    "cell_width": 48,
    "cell_height": 64
}

elements: dict[str, Any] = {
    "floor": (2, 3),
    "horizontal_wall": (0, 0),
    "vertical_wall": (16, 0),
}

# set_map = {
#     (0x0) : ["floor"],
#     (0xf) : ["north", "east", "south", "west"],
#     (0x1) : ["north"],
#     (0x)
# }

