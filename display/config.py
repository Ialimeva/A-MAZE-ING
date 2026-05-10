from typing import Any
from dataclasses import dataclass

@dataclass
class DisplayConfig:
    columns: int
    rows: int
    cell_width: int = 48
    cell_height: int = 64
    floor: tuple = (2, 3)
    horizontal_wall: tuple = (0, 0)
    vertical_wall: tuple = (16, 0)

# set_map = {
#     (0x0) : ["floor"],
#     (0xf) : ["north", "east", "south", "west"],
#     (0x1) : ["north"],
#     (0x)
# }