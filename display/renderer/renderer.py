# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/13 14:47:29 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..utils import offset
from ..config import DisplayConfig
from display import np, Maze
from .spritsheet import Spritesheet

class Draw:
    def __init__(self,
                 img_data: tuple,
                 buff_data: tuple,
                 display_config: DisplayConfig,
                 maze: Maze
                ):
        
        self.configs = display_config

        # Image and Buff data are still in Ctypes wrapped memory
        (self.img_ptr,
         self.img_adr,
         self.img_line,
         self.img_width,
         self.img_height,
        ) = img_data
        (self.buff_ptr, self.buff_adr, self.buff_line) = buff_data

        # Image and Buff are in raw C memory adresses
        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)

        self.buff_width = self.configs.columns * self.configs.cell_width
        self.buff_height = self.configs.rows * self.configs.cell_height
        self.img_3d = self.img_array.reshape(
                                    self.img_height,
                                    self.img_width,
                                    4
                                )
        self.buff_3d = self.buff_array.reshape(
                                    self.buff_height,
                                    self.buff_width,
                                    4
                                )
        
        self.spritesheet = Spritesheet(self.img_3d)
        self.maze_hex = maze.grid_hex

    def floor(self) -> None:
        src_x, src_y = self.configs.floor
        color = self.img_3d[(src_y * 16), (src_x * 16)]
        for y in range(self.buff_height):
            self.buff_3d[y] = color

    @property
    def horizontal_wall(self) -> list[list[list]]:
        x_min, x_max = self.configs.horizontal_wall_x
        y_min, y_max = self.configs.horizontal_wall_y
        horizontall_wall = self.spritesheet.get_tileset(
                                (x_min * 16),
                                (x_max * 16),
                                (y_min * 16),
                                (y_max * 16)
                            )
        h_wall_height, h_wall_width, _ = horizontall_wall.shape
        return (horizontall_wall, h_wall_width, h_wall_height)
    
    @property
    def vertical_wall(self) -> list[list[list]]:
        x_min, x_max = self.configs.vertical_wall_x
        y_min, y_max = self.configs.vertical_wall_y
        vertical_wall = self.spritesheet.get_tileset(
                            (x_min * 16),
                            (x_max * 16),
                            (y_min * 16),
                            (y_max * 16)
                        )
        v_wall_height, v_wall_width, _ = vertical_wall.shape
        return (vertical_wall, v_wall_width, v_wall_height)

    def cell(self) -> None:
        h_wall, h_wall_width, h_wall_height = self.horizontal_wall
        v_wall, v_wall_width, v_wall_height = self.vertical_wall
        dest_y = 0
        for y in range(len(self.maze_hex)):
            dest_x = 0
            for x in range(len(self.maze_hex[0])):
                hex_value = int(self.maze_hex[y][x], 16)
                if (hex_value & 1):
                    self.buff_3d[
                        dest_y : h_wall_height,
                        dest_x : h_wall_width
                    ] = h_wall
                if (hex_value >> 1 & 1):
                    self.buff_3d[
                        dest_y : v_wall_height,
                        (
                            (dest_x + self.configs.cell_width) - v_wall_width
                        ) : (dest_x + self.configs.cell_width),
                    ] = v_wall

                if (hex_value >> 2 & 1):
                    self.buff_3d[
                        (
                            (dest_y + self.configs.cell_height) - h_wall_height
                        ) : (dest_y + self.configs.cell_height),
                        dest_x : h_wall_width
                    ] = h_wall

                if (hex_value >> 3 & 1):
                    self.buff_3d[
                            dest_y : v_wall_height,
                            dest_x : v_wall_width
                    ] = v_wall

                dest_x = dest_x + self.configs.cell_width
            dest_y = dest_y + self.configs.cell_height
