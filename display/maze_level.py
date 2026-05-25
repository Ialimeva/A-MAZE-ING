# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_level.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 14:51:46 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/25 18:01:03 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from typing import Any
from display import np
from .engine.window import Window
from .engine.input_manager import input_manager
from .renderer.renderer import Draw
from .display_config import DisplayConfig
from core import MazeManager
from mazegen import Maze


class Game:
    def __init__(self, configs: dict):
        self.configs = configs
        self.display_config = DisplayConfig(
            columns = self.configs["width"],
            rows = self.configs["height"],
            entry_point = self.configs["entry"],
            exit_point = self.configs["exit"],
        )
        self.window = Window(self.display_config)
        self.img_data = self.window.img_data()
        self.buff_data = self.window.buff_data()
        self.draw = Draw(self.img_data, self.buff_data, self.display_config)
        self.maze = Maze()
        self.gen = MazeManager.generate_step(self.configs)
        
        self.buff_cache = None
        
        self.regen_maze = False
        self.path_show = False

    def run(self) -> None:
        self.window.start(self.update)

    def update(self, param: Any) -> None:
        if input_manager["ESC"]:
            self.window.exit_window(None)

        if input_manager["ENTER"]:
            try:
                self.maze = next(self.gen)
                self.draw.maze_hex = self.maze.grid_hex
            except StopIteration:
                self.buff_cache = np.copy(self.draw.buff_3d)
                self.done_gen = True
                input_manager["ENTER"] = False
            self.draw.maze()  
            self.window.render_image()
            
            if self.done_gen:
                self.solve = MazeManager.solve_step(self.maze, self.configs)
        
        if input_manager["S"]: #and self.buff_cache is None: //TODO: 1 buttun for entry exit and solve            
            self.draw.path = []
            try:
                self.draw.path.append(MazeManager.grid_to_cell(next(self.solve)))
            except StopIteration as e:
                self.draw.buff_3d[:] = self.buff_cache
                self.draw.path = [MazeManager.grid_to_cell(coord) for coord in e.value]
                input_manager["S"] = False

            self.draw.render_path()
            self.draw.entry_and_exit()
            self.window.render_image()

        if input_manager["P"]:
            if self.path_show:
               self.draw.render_path()
               self.draw.entry_and_exit()
               self.window.render_image()
               self.path_show = False
               input_manager["P"] = False
            elif not self.path_show:
                self.draw.buff_3d[:] = self.buff_cache
                self.window.render_image()
                self.path_show = True
                input_manager["P"] = False

        # //TODO: Potential bug on self.done_gen condition
        if input_manager["G"]:
            if not self.regen_maze:
                self.regen_maze = True
                self.path_show = False
            elif self.regen_maze:
                self.configs["seed"] = random.randint(0, 10000)
                self.gen = MazeManager.generate_step(self.configs)
                try:
                    self.maze = next(self.gen)
                    self.draw.maze_hex = self.maze.grid_hex
                except StopIteration:
                    self.buff_cache = np.copy(self.draw.buff_3d)
                    input_manager["G"] = False
                self.draw.maze()  
                self.window.render_image()
                
                if self.done_gen:
                    self.solve = MazeManager.solve_step(self.maze, self.configs)
