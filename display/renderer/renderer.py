# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/24 10:40:30 by ialrandr        ###   ########.fr        #
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

    #//TODO Optimize code readebility for floor rendering and color change
    def floor(self) -> None:
        src_x, src_y = self.display_configs.floor
        color = self.img_3d[(src_y * 16), (src_x * 16)]
        # color[0], color[1], color[2], color[3] = (97, 71, 147, 255)
        color2 = [215, 240, 246, 255]

        dest_y: int = 0
        for y in range(len(self.maze_hex)):
            dest_x: int = 0
            for x in range(len(self.maze_hex[0])):
                hex_value: str = self.maze_hex[y][x]
                if (hex_value == "F"):
                    self.buff_3d[
                        dest_y : dest_y + self.display_configs.cell_height,
                        dest_x : dest_x + self.display_configs.cell_width
                    ] = color2
                else:
                    self.buff_3d[
                        dest_y : dest_y + self.display_configs.cell_height,
                        dest_x : dest_x + self.display_configs.cell_width
                    ] = color
                dest_x = dest_x + self.display_configs.cell_width
            dest_y = dest_y + self.display_configs.cell_height


    def tileset(self, x_coordinates: tuple, y_coordinates: tuple) -> tuple:
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
        h_wall, h_wall_height, h_wall_width = self.tileset(
            self.display_configs.horizontal_wall_x,
            self.display_configs.horizontal_wall_y
        )

        v_wall, v_wall_height, v_wall_width = self.tileset(
            self.display_configs.vertical_wall_x,
            self.display_configs.vertical_wall_y
        )

        b_wall, b_wall_height, b_wall_width = self.tileset(
            self.display_configs.bottom_wall_x,
            self.display_configs.bottom_wall_y,
        )

        sv_wall, sv_wall_height, sv_wall_width = self.tileset(
            self.display_configs.side_v_wall_x,
            self.display_configs.side_v_wall_y,
        )

        h_joint, h_joint_height, h_joint_width = self.tileset(
            self.display_configs.horizontal_joint_x,
            self.display_configs.horizontal_joint_y,
        )

        empty_joint, empty_joint_height, empty_joint_width = self.tileset(
            self.display_configs.empty_joint_x,
            self.display_configs.empty_joint_y,
        )
        #// TODO: code structuration(repetition) 
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
                        dest_x : dest_x + empty_joint_width #//TODO: FIX EMPTY JOINT WALLS SPACE
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
                        dest_y + sv_wall_height - h_joint_height : dest_y + sv_wall_height + h_joint_height,
                        dest_x : dest_x + h_joint_width 
                    ] = h_joint

                    self.buff_3d[
                        dest_y + sv_wall_height - b_wall_height : (
                            dest_y + sv_wall_height + b_wall_height
                        ),
                        dest_x + v_wall_width : dest_x + v_wall_width + b_wall_width
                    ] = b_wall

                    # Draw rightmost bottom wall
                    if (x == len(self.maze_hex[0]) - 1):
                        self.buff_3d[
                            dest_y : dest_y + sv_wall_height,
                            dest_x + v_wall_width + h_wall_width:
                            (dest_x + (v_wall_width * 2) + h_wall_width)
                        ] = sv_wall

                dest_x = dest_x + v_wall_width + h_wall_width
            dest_y = dest_y + v_wall_height

    
    def entry_and_exit(self) -> None:
        entry_x, entry_y = self.display_configs.entry_point
        exit_x, exit_y = self.display_configs.exit_point

        hole, hole_height, hole_width  = self.tileset(
            self.display_configs.hole_x,
            self.display_configs.hole_y
        )
        
        dest_entry_x = entry_x * self.display_configs.cell_width
        dest_entry_y = entry_y * self.display_configs.cell_height
        self.buff_3d[
            dest_entry_y + 30: dest_entry_y + hole_height + 30,
            dest_entry_x + 20 : dest_entry_x + hole_width + 20,
        ] = hole