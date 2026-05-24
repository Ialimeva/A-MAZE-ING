from dataclasses import dataclass

@dataclass
class DisplayConfig:
    columns: int
    rows: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    cell_width: int = 47
    cell_height: int = 36

    extra_width = 5
    extra_height = 16
    
    floor: tuple = (2, 3)
    
    horizontal_wall_x: tuple = (3, 45)
    horizontal_wall_y: tuple = (0, 32)
    
    vertical_wall_x: tuple = (256, 272)
    vertical_wall_y: tuple = (0, 48)

    bottom_wall_x: tuple = (3, 45)
    bottom_wall_y: tuple = (0, 32)
    
    
    side_v_wall_x: tuple = (256, 272)
    side_v_wall_y: tuple = (0, 64)
    
    horizontal_joint_x = (3, 8)
    horizontal_joint_y = (0, 32)
    
    empty_joint_x = (3, 7)
    empty_joint_y = (0, 32)

    hole_x = (8 * 16, 9 * 16)
    hole_y = (9 * 16, 11 * 16)