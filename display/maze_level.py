# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_level.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 14:51:46 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/11 15:46:53 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from .engine.window import Window
from .engine.input_manager import input_manager
from .renderer.renderer import Draw
from .config import DisplayConfig
from display import Maze

class Game:
    def __init__(self, display_config: DisplayConfig, maze: Maze):
        self.window = Window(display_config)
        self.img_data: tuple = self.window.img_data()
        self.buff_data: tuple = self.window.buff_data()
        self.draw = Draw(
                        self.img_data,
                        self.buff_data,
                        display_config,
                        maze
                    )

    def run(self) -> None:
        self.window.start(self.update)

    def update(self, param: Any) -> None:
        if (input_manager["ESC"]):
            self.window.exit_window(None)
        if (input_manager["ENTER"]):
            self.draw.floor()
            self.window.render_image()