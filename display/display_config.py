from dataclasses import dataclass


@dataclass
class DisplayConfig:
    columns: int
    rows: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    cell_width = 47
    cell_height = 36

    extra_width = 5
    extra_height = 16

    display_width = 1920
    display_height = 1020

    floor = (2, 3)

    horizontal_wall_x = (3, 45)
    horizontal_wall_y = (0, 32)

    vertical_wall_x = (256, 272)
    vertical_wall_y = (0, 48)

    bottom_wall_x = (3, 45)
    bottom_wall_y = (0, 32)

    side_v_wall_x = (256, 272)
    side_v_wall_y = (0, 64)

    horizontal_joint_x = (3, 8)
    horizontal_joint_y = (0, 32)

    empty_joint_x = (3, 7)
    empty_joint_y = (0, 32)

    dude_x = (10 * 16, 11 * 16)
    dude_y = (14 * 16, 15 * 16)

    money_x = (15 * 16, 16 * 16)
    money_y = (13 * 16, 14 * 16)
