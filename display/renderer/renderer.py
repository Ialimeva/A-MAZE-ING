# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/10 15:42:20 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import numpy as np
from ..utils import offset
from ..config import DisplayConfig

class Draw:
    def __init__(self,
                 img_data: tuple,
                 buff_data: tuple,
                 display_config: DisplayConfig
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
        self.three_dimension_img = self.img_array.reshape(
                                    self.img_height,
                                    self.img_width,
                                    4
                                )
        self.three_dimension_buff = self.buff_array.reshape(
                                    self.buff_height,
                                    self.buff_width,
                                    4
                                )

    def floor(self) -> None:
        src_x, src_y = self.configs.floor
        color = self.three_dimension_img[(src_y * 16), (src_x * 16)]
        for y in range(self.buff_height):
            self.three_dimension_buff[y] = color

    # def horizontal_wall(self) -> None:
    #     src_x, src_y = elements["horizontal_wall"]
    #     off_src = offset((src_x * 16), (src_y * 16), self.img_line)
    #     color = self.img_array[off_src : off_src + 4]
    #     while not color[3]:
    #         off_src = offset((src_x * 16), ((src_y + 1) * 16), self.img_line)
    #         color = self.img_array[off_src + off_src + 4]
    #     limit_x, limit_y = maze_config["limit_horizontal_wall"]
    #     off_limit = offset((limit_x * 16), (limit_y * 16), self.img_line)
    #     row_src = off_src // self.img_line
    #     row_limit = off_limit // self.img_line
    #     row_distance = abs(row_limit - row_src)
    #     wall = self.img_array[off_src : (off_src + maze_config["cell_width"])]
