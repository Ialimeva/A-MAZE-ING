# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/06/03 13:43:29 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from ..display_config import DisplayConfig
from display import np, Maze
from .spritsheet import Spritesheet
from .renderer_utils import (
    scale_pixel,
    recolor_pixel,
    tileset,
    floor_colors,
    wall_colors,
    background_colors
)

class Draw:
    def __init__(self,
                 img_data: tuple,
                 buff_data: tuple,
                 display_data: tuple,
                 display_configs: DisplayConfig,
                ):
        
        self.display_configs = display_configs

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
        print(self.buff_height)

        (self.display_ptr,
         self.display_adr,
         self.display_line,
         self.display_width,
         self.display_height
        ) = display_data

        # Image and Buff are in raw C memory adresses
        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)
        self.display_array = np.frombuffer(self.display_adr, dtype=np.uint8)
        
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
        
        self.display_3d = self.display_array.reshape(
                                    self.display_height,
                                    self.display_width,
                                    4
                                )
        
        self.spritesheet = Spritesheet(self.img_3d)
        self.h_wall, self.h_wall_height, self.h_wall_width = tileset(
            self.display_configs.horizontal_wall_x,
            self.display_configs.horizontal_wall_y,
            self.spritesheet
        )        
        
        self.v_wall, self.v_wall_height, self.v_wall_width = tileset(
            self.display_configs.vertical_wall_x,
            self.display_configs.vertical_wall_y,
            self.spritesheet
        )

        self.b_wall, self.b_wall_height, self.b_wall_width = tileset(
            self.display_configs.bottom_wall_x,
            self.display_configs.bottom_wall_y,
            self.spritesheet
        )

        self.sv_wall, self.sv_wall_height, self.sv_wall_width = tileset(
            self.display_configs.side_v_wall_x,
            self.display_configs.side_v_wall_y,
            self.spritesheet
        )

        self.h_joint, self.h_joint_height, self.h_joint_width = tileset(
            self.display_configs.horizontal_joint_x,
            self.display_configs.horizontal_joint_y,
            self.spritesheet
        )

        self.empty_joint, self.empty_joint_height, self.empty_joint_width = tileset(
            self.display_configs.empty_joint_x,
            self.display_configs.empty_joint_y,
            self.spritesheet
        )

        self.dude, self.dude_height, self.dude_width  = tileset(
            self.display_configs.dude_x,
            self.display_configs.dude_y,
            self.spritesheet
        )
        self.money, self.money_height, self.money_width  = tileset(
            self.display_configs.money_x,
            self.display_configs.money_y,
            self.spritesheet
        )

        self.dude = scale_pixel(self.dude, 2)
        self.dude_height, self.dude_width, _ = self.dude.shape

        self.money = scale_pixel(self.money, 2)
        self.money_height, self.money_width, _ = self.money.shape


        self.maze_hex = []
        self.path = []

        self.theme_cache = {}
        self.fcolors = floor_colors
        self.wcolors = wall_colors
        self.bcolors = background_colors
        self.wcolors_keys = list(self.wcolors.keys())

        for theme in self.wcolors_keys:
            w1, w2, w3 = self.wcolors[theme]
            f1, f2, f3 = self.fcolors[theme]
            bcolor = self.bcolors[theme]
            
            t_hw = self.h_wall.copy()
            t_vw = self.v_wall.copy()
            t_svw = self.sv_wall.copy()
            t_bw = self.b_wall.copy()
            t_hj = self.h_joint.copy()
            t_ej = self.empty_joint.copy()

            for sprite in [t_hw, t_vw, t_svw, t_bw, t_hj, t_ej]:
                recolor_pixel(sprite, [53, 40, 66, 255], w1)
                recolor_pixel(sprite, [23, 17, 28, 255], w2)
                recolor_pixel(sprite, [96, 103, 117, 255], w3)

            self.theme_cache[theme] = {
                "h_wall": t_hw,
                "v_wall": t_vw,
                "b_wall": t_bw,
                "sv_wall": t_svw,
                "hj_wall": t_hj,
                "ej_wall": t_ej,
                "f1": f1,
                "f2": f2,
                "f3": f3,
                "bcolor": bcolor,
            }

        self.active_theme = self.theme_cache["default_theme"]
        (self.h_wall,
         self.v_wall,
         self.b_wall,
         self.sv_wall,
         self.h_joint,
         self.empty_joint,
         self.fcolor1,
         self.fcolor2,
         self.fcolor3,
         self.bcolor
        ) = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"],
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"],
        )
        
        self.camera_x, self.camera_y = (0, 0)
        self.speed = 20

    def blit(self, y_coords, x_coords, wall) -> None:
        start_x, end_x = x_coords
        start_y, end_y = y_coords
        
        self.buff_3d[start_y : end_y, start_x : end_x] = wall

    def floor(self) -> None:
        dest_y: int = 0
        for y in range(len(self.maze_hex)):
            dest_x: int = 0
            for x in range(len(self.maze_hex[0])):
                hex_value: str = self.maze_hex[y][x]
                if (hex_value == "F"):
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor2
                    )
                else:
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor1
                    )
                dest_x = dest_x + self.display_configs.cell_width
            dest_y = dest_y + self.display_configs.cell_height
    

    def cell(self) -> None:
        dest_y = 0
        for y in range(len(self.maze_hex)):
            dest_x = 0
            for x in range(len(self.maze_hex[0])):
                hex_value = int(self.maze_hex[y][x], 16)

                if (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x, dest_x + self.v_wall_width),
                        self.v_wall
                    )

                if (hex_value & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_wall_height),
                        (dest_x + self.v_wall_width, 
                         dest_x + self.v_wall_width + self.h_wall_width),
                        self.h_wall
                    )
                
                if (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint
                    )

                if not (hex_value & 1) and  not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.empty_joint_height),
                        (dest_x, dest_x + self.empty_joint_width),
                        self.empty_joint
                    )

                if (x == len(self.maze_hex[0]) - 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x + self.v_wall_width + self.h_wall_width,
                        (dest_x + (self.v_wall_width * 2) + self.h_wall_width)),
                        self.v_wall
                    )

                if (y == len(self.maze_hex) - 1):
                    # Draw bottom walls
                    self.blit(
                        (dest_y + self.sv_wall_height - self.h_joint_height,
                         dest_y + self.sv_wall_height + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint 
                    )

                    self.blit(
                        (dest_y + self.sv_wall_height - self.b_wall_height,
                         dest_y + self.sv_wall_height + self.b_wall_height),
                        (dest_x + self.v_wall_width,
                         dest_x + self.v_wall_width + self.b_wall_width),
                        self.b_wall
                    )

                    if (x == len(self.maze_hex[0]) - 1):
                        self.blit(
                            (dest_y, dest_y + self.sv_wall_height),
                            (dest_x + self.v_wall_width + self.h_wall_width,
                             dest_x + (self.v_wall_width * 2) + self.h_wall_width),
                            self.sv_wall
                        )

                dest_x = dest_x + self.v_wall_width + self.h_wall_width
            dest_y = dest_y + self.v_wall_height

    
    def entry_and_exit(self) -> None:
        entry_x, entry_y = self.display_configs.entry_point
        exit_x, exit_y = self.display_configs.exit_point

        dest_entry_x = entry_x * self.display_configs.cell_width
        dest_entry_y = entry_y * self.display_configs.cell_height

        dest_exit_x = exit_x * self.display_configs.cell_width
        dest_exit_y = exit_y * self.display_configs.cell_height
        
        self.blit(
            (dest_entry_y + 10, dest_entry_y + self.dude_height + 10),
            (dest_entry_x + 12, dest_entry_x + self.dude_width + 12),
            self.dude 
        )

        self.blit(
            (dest_exit_y + 10, dest_exit_y + self.money_height + 10),
            (dest_exit_x + 12, dest_exit_x + self.money_width + 12),
            self.money
        )

    
    def render_path(self):
        for coord in self.path:
            x, y = coord

            dest_x = x * self.display_configs.cell_width
            dest_y = y * self.display_configs.cell_height

            self.blit(
                (dest_y, dest_y + self.display_configs.cell_height),
                (dest_x, dest_x + self.display_configs.cell_width),
                self.fcolor3
            )
        self.cell()

    def maze(self) -> None:
        self.floor()
        self.cell()

    def change_wall_color(self):
        n: int = random.randint(0, len(wall_colors) - 1)
        key: str = self.wcolors_keys[n]
        self.active_theme = self.theme_cache[key]
        
        (self.h_wall,
         self.v_wall,
         self.b_wall,
         self.sv_wall,
         self.h_joint,
         self.empty_joint,
         self.fcolor1,
         self.fcolor2,
         self.fcolor3,
         self.bcolor
        ) = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"],
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"]
        )


    def present(self) -> None:
        self.display_3d[:] = self.bcolor

        visible_h = min(self.buff_height, self.display_height)
        visible_w = min(self.buff_width, self.display_width)

        offset_x = max(0, (self.display_width - self.buff_width) // 2)
        offset_y = max(0, (self.display_height - self.buff_height) // 2)
        
        self.camera_x = max(0, min(
                self.camera_x, self.buff_width - self.display_width
            )
        )
        self.camera_y = max(0, min(
                self.camera_y, self.buff_height - self.display_height
            )
        )

        self.display_3d[
            offset_y : offset_y + visible_h,
            offset_x : offset_x + visible_w
        ] = self.buff_3d[
            self.camera_y : self.camera_y + visible_h,
            self.camera_x : self.camera_x + visible_w,
        ]
