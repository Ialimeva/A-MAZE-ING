# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/04 13:12:18 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/05 10:48:55 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import numpy as np
from ..utils import offset
from ..config import elements, maze_config

class Draw:
    def __init__(self, img_data: tuple, buff_data: tuple):
        # Image and Buff data are still in Ctypes wrapped memory
        (self.img_ptr, self.img_adr, self.img_line) = img_data
        (self.buff_ptr, self.buff_adr, self.buff_line) = buff_data

        # Image and Buff are in raw C memory adresses
        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)

        self.width = maze_config["colums"] * maze_config["cell_width"]
        self.height = maze_config["rows"] * maze_config["cell_height"]

    def floor(self) -> None:
        src_x, src_y = elements["floor"]
        off_src = offset((src_x * 16), (src_y * 16), self.img_line)
        color = self.img_array[off_src : off_src + 4]
        row = np.tile(color, self.width)
        for y in range(self.height):
            off_dst = offset(0, y, self.buff_line)
            self.buff_array[off_dst : off_dst + self.buff_line] = row

    def horizontal_wall(self) -> None:
        src_x, src_y = elements["horizontal_wall"]
        off_src = offset((src_x * 16), (src_y * 16), self.img_line)
        color = self.img_array[off_src : off_src + 4]
        while not color[3]:
            off_src = offset((src_x * 16), ((src_y + 1) * 16), self.img_line)
            color = self.img_array[off_src + off_src + 4]
        limit_x, limit_y = maze_config["limit_horizontal_wall"]
        off_limit = offset((limit_x * 16), (limit_y * 16), self.img_line)
        row_src = off_src // self.img_line
        row_limit = off_limit // self.img_line
        row_distance = abs(row_limit - row_src)
        wall = self.img_array[off_src : (off_src + maze_config["cell_width"])]
