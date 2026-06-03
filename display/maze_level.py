# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_level.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: meva <meva@student.42.fr>                 +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 14:51:46 by ialrandr        #+#    #+#               #
#  Updated: 2026/06/01 07:54:20 by meva            ###   ########.fr        #
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


class Game:
    def __init__(self, configs: dict):
        self.configs: dict = configs
        self.display_config: DisplayConfig = DisplayConfig(
            columns = self.configs["width"],
            rows = self.configs["height"],
            entry_point = self.configs["entry"],
            exit_point = self.configs["exit"],
        )
        self.window = Window(self.display_config)
        self.img_data = self.window.img_data()
        self.buff_data = self.window.buff_data()
        self.display_data = self.window.display_data()
        self.draw = Draw(
            self.img_data,
            self.buff_data,
            self.display_data,
            self.display_config
        )
        self.maze = []
        self.gen = MazeManager.generate_step(self.configs)
        
        self.buff_cache = None
        
        self.path_show = False
        self.regen_maze = False
        self.done_gen = False
        self.done_solve = False
        self.change_wcolor = False
        self.solve = []
        self.draw.path = []

    
    def run(self) -> None:
        self.window.welcome_page()
        self.window.start(self.update)

    
    def generate_step(self, generator, key: str) -> None:
        if self.done_gen:
            input_manager[key] = False
            return
        try:
            self.maze = next(generator)
            self.draw.maze_hex = self.maze.grid_hex
        except StopIteration:
            input_manager[key] = False
            self.done_gen = True
            self.buff_cache = np.copy(self.draw.buff_3d)
            try:
                self.solve = MazeManager.solve_step(self.maze, self.configs)
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
            input_manager[key] = False
            print(f"Error: {e}")
        
        if not self.done_gen:
            self.draw.maze()
            self.draw.present()
            self.window.render_image()
            

    def update(self, param: Any) -> None:
        try:
            if input_manager["ESC"]:
                self.window.exit_window(None)
                input_manager["ESC"] = False

            if input_manager["ENTER"]:
                self.generate_step(self.gen, "ENTER")

            if input_manager["G"]:
                if not self.regen_maze:
                    self.regen_maze = True
                    self.draw.path = []
                    self.path_show = False
                    self.done_gen = False
                    self.done_solve = False
                    self.configs["seed"] = random.randint(0, 10000)
                    self.gen = MazeManager.generate_step(self.configs)
                self.generate_step(self.gen, "G")
                if self.done_gen:
                    self.regen_maze = False

            if input_manager["S"] and self.done_gen:
                if self.done_solve:
                    input_manager["S"] = False
                    return
                try:
                    self.draw.path.append(MazeManager.grid_to_cell(next(self.solve)))
                except StopIteration as e:
                    input_manager["S"] = False
                    self.draw.buff_3d[:] = self.buff_cache
                    try:
                        self.draw.path = [MazeManager.grid_to_cell(coord) for coord in e.value]
                        self.done_solve = True
                    except Exception as e:
                        print(f"Error: {e}")
                        return
                except Exception as e:
                    input_manager["S"] = False
                    print(f"Error: {e}")
                    return

                self.draw.render_path()
                self.draw.entry_and_exit()
                self.draw.present()
                self.window.render_image()

            if input_manager["P"] and self.done_solve:
                try:
                    if self.path_show:
                        input_manager["P"] = False
                        self.draw.render_path()
                        self.draw.entry_and_exit()
                        self.draw.present()
                        self.window.render_image()
                        self.path_show = False
                    elif not self.path_show:
                        input_manager["P"] = False
                        self.draw.buff_3d[:] = self.buff_cache
                        self.draw.present()
                        self.window.render_image()
                        self.path_show = True
                except Exception as e:
                    input_manager["P"] = False
                    print(f"Error: {e}")

            if input_manager["C"] and self.done_gen:
                input_manager["C"] = False
                try:
                    self.draw.change_wall_color()
                    self.draw.maze()
                    self.buff_cache = np.copy(self.draw.buff_3d)
                    if self.done_solve and not self.path_show:
                        self.draw.render_path()
                        self.draw.entry_and_exit()
                    self.draw.present()
                    self.window.render_image()
                except Exception as e:
                    print(f"Error: {e}")

            if input_manager["UP"]:
                self.draw.camera_y -= self.draw.speed
                self.draw.present()
                self.window.render_image()
            
            if input_manager["DOWN"]:
                self.draw.camera_y += self.draw.speed
                self.draw.present()
                self.window.render_image()
            
            if input_manager["LEFT"]:
                self.draw.camera_x -= self.draw.speed
                self.draw.present()
                self.window.render_image()
            
            if input_manager["RIGHT"]:
                self.draw.camera_x += self.draw.speed
                self.draw.present()
                self.window.render_image()

        except (KeyboardInterrupt, EOFError):
            return
        except Exception as e:
            print(f"Error: {e}")
