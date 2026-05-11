from typing import Any
from dataclasses import dataclass

@dataclass
class DisplayConfig:
    columns: int
    rows: int
    cell_width: int = 48
    cell_height: int = 64
    floor: tuple = (2, 3)
    horizontal_wall_x: tuple = (0, 3)
    horizontal_wall_y: tuple = (0, 2)
    vertical_wall_x: tuple = (16, 17)
    vertical_wall_y: tuple = (0, 3)

# set_map = {
#     (0x0) : ["floor"],
#     (0xf) : ["north", "east", "south", "west"],
#     (0x1) : ["north"],
#     (0x)
# }