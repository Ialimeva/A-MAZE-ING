# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/23 13:00:38 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..display_config import DisplayConfig
from display import np, Maze
from .spritsheet import Spritesheet

class Draw:
    def __init__(self,
                 img_data: tuple,
                 buff_data: tuple,
                 display_config: DisplayConfig,
                ):
        
        self.display_configs = display_config

        # Image and Buff data are still in Ctypes wrapped memory
        (self.img_ptr,
         self.img_adr,
         self.img_line,
         self.img_width,
         self.img_height,
        ) = img_data
        
        (self.buff_ptr,
         self.buff_adr,
         self.buff_line,
         self.buff_width,
         self.buff_height
        ) = buff_data

        # Image and Buff are in raw C memory adresses
        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)

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
        self.maze_hex = []

    def floor(self) -> None:
        src_x, src_y = self.display_configs.floor
        color = self.img_3d[(src_y * 16), (src_x * 16)]
        color[0], color[1], color[2], color[3] = (147, 71, 97, 255)
        for y in range(self.buff_height):
            self.buff_3d[y] = color     #//TODO Render floor per cell 

    def wall(self, x_coordinates: tuple, y_coordinates: tuple) -> tuple:
        x_min, x_max = x_coordinates
        y_min, y_max = y_coordinates
        tileset = self.spritesheet.get_tileset(
                    x_min,
                    x_max,
                    y_min,
                    y_max
                )
        tileset_height, tileset_witdth, _ = tileset.shape
        return (tileset, tileset_height, tileset_witdth)
    
    
    def cell(self) -> None:
        h_wall, h_wall_height, h_wall_width = self.wall(
            self.display_configs.horizontal_wall_x,
            self.display_configs.horizontal_wall_y
        )

        v_wall, v_wall_height, v_wall_width = self.wall(
            self.display_configs.vertical_wall_x,
            self.display_configs.vertical_wall_y
        )

        b_wall, b_wall_height, b_wall_width = self.wall(
            self.display_configs.bottom_wall_x,
            self.display_configs.bottom_wall_y,
        )

        sv_wall, sv_wall_height, sv_wall_width = self.wall(
            self.display_configs.side_v_wall_x,
            self.display_configs.side_v_wall_y,
        )

        h_joint, h_joint_height, h_joint_width = self.wall(
            self.display_configs.horizontal_joint_x,
            self.display_configs.horizontal_joint_y,
        )

        empty_joint, empty_joint_height, empty_joint_width = self.wall(
            self.display_configs.empty_joint_x,
            self.display_configs.empty_joint_y,
        )

        dest_y = 0
        for y in range(len(self.maze_hex)):
            dest_x = 0
            for x in range(len(self.maze_hex[0])):
                hex_value = int(self.maze_hex[y][x], 16)

                # Draw vertical wall at dest_x = 0
                if (hex_value >> 3 & 1):
                    self.buff_3d[
                        dest_y : dest_y + v_wall_height,
                        dest_x : dest_x + v_wall_width 
                    ] = v_wall

                # Draw horizontal wall at dest_x = dest_x + v_wall_width
                if (hex_value & 1):
                    self.buff_3d[
                        dest_y : dest_y + h_wall_height,
                        dest_x + v_wall_width : dest_x + v_wall_width + h_wall_width
                    ] = h_wall
                
                # Draw horizontal wall joint when there is no v_wall
                if (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.buff_3d[
                        dest_y : dest_y + h_joint_height,
                        dest_x : dest_x + h_joint_width
                    ] = h_joint

                # Draw joint when no north and lest wall
                if not (hex_value & 1) and  not (hex_value >> 3 & 1):
                    self.buff_3d[
                        dest_y : dest_y + empty_joint_height,
                        dest_x : dest_x + empty_joint_width
                    ] = empty_joint

                # Draw rightmost wall
                if (x == len(self.maze_hex[0]) - 1):
                    self.buff_3d[
                        dest_y : dest_y + v_wall_height,
                        dest_x + v_wall_width + h_wall_width:
                        (dest_x + (v_wall_width * 2) + h_wall_width)
                    ] = v_wall

                # Draw last row
                if (y == len(self.maze_hex) - 1):
                    # Draw bottom walls
                    self.buff_3d[
                        dest_y + sv_wall_height - b_wall_height : (
                            dest_y + sv_wall_height + b_wall_height
                        ),
                        dest_x + v_wall_width : dest_x + v_wall_width + b_wall_width
                    ] = b_wall

                    if (hex_value >> 3 & 1):
                        # Draw last vertical wall
                        self.buff_3d[
                            dest_y : dest_y + sv_wall_height,
                            dest_x : dest_x + sv_wall_width  
                        ] = sv_wall

                dest_x = dest_x + v_wall_width + h_wall_width
            dest_y = dest_y + v_wall_height