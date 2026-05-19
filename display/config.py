from typing import Any
from dataclasses import dataclass

@dataclass
class DisplayConfig:
    columns: int
    rows: int
    cell_width: int = 47
    cell_height: int = 36

    last_wall_width = 5
    last_wall_height = 16
    
    floor: tuple = (2, 3)
    
    horizontal_wall_x: tuple = (3, 45)
    horizontal_wall_y: tuple = (0, 2)
    
    south_wall_y: tuple = (0, 23)
    
    vertical_wall_x: tuple = (16, 17)
    vertical_wall_y: tuple = (0, 3)
    
    last_vertical_wall_y: tuple = (0, 4)
    
    horizontal_wall_joint_x = (3, 8)
    horizontal_wall_joint_y = (0, 2)