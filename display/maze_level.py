import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

import random
from typing import Any, Generator
from .engine.window import Window
from .engine.input_manager import Hooks
from .renderer.renderer import Draw
from .display_config import DisplayConfig
from core import MazeManager
from mazegen import Maze


class Game:
    def __init__(self, configs: dict[str, Any]) -> None:
        self.configs = configs
        self.display_config = DisplayConfig(
            columns=self.configs["width"],
            rows=self.configs["height"],
            entry_point=self.configs["entry"],
            exit_point=self.configs["exit"],
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
        self.maze: Maze = Maze()
        self.gen = MazeManager.generate_step(self.configs)

        self.buff_cache = np.ndarray([])

        self.path_show = False
        self.regen_maze = False
        self.done_gen = False
        self.done_solve = False
        self.change_wcolor = False
        self.solve: Generator[
            tuple[int, int], None, list[tuple[int, int]]
        ]
        self.draw.path = []

    def run(self) -> None:
        self.window.welcome_page()
        self.window.start(self.update)

    def generate_step(
            self,
            generator: Generator[Maze, None, None],
            key: str
    ) -> None:
        if self.done_gen:
            Hooks.input_manager[key] = False
            return
        try:
            self.maze = next(generator)
            self.draw.maze_hex = self.maze.grid_hex
        except StopIteration:
            Hooks.input_manager[key] = False
            self.done_gen = True
            self.buff_cache = np.copy(self.draw.buff_3d)
            try:
                self.solve = MazeManager.solve_step(self.maze, self.configs)
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
            Hooks.input_manager[key] = False
            print(f"Error: {e}")

        if not self.done_gen:
            self.draw.maze()
            self.draw.present()
            self.window.render_image()

    def update(self, _: Any) -> None:
        try:
            if Hooks.input_manager["ESC"]:
                self.window.exit_window(None)
                Hooks.input_manager["ESC"] = False

            if Hooks.input_manager["ENTER"]:
                self.generate_step(self.gen, "ENTER")

            if Hooks.input_manager["G"]:
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

            if Hooks.input_manager["S"] and self.done_gen:
                if self.done_solve:
                    Hooks.input_manager["S"] = False
                    return
                try:
                    self.draw.path.append(
                        MazeManager.grid_to_cell(next(self.solve))
                    )
                except StopIteration as e:
                    Hooks.input_manager["S"] = False
                    self.draw.buff_3d[:] = self.buff_cache
                    try:
                        self.draw.path = [
                            MazeManager.grid_to_cell(coord)
                            for coord in e.value
                        ]
                        self.done_solve = True
                    except Exception as e:
                        print(f"Error: {e}")
                        return
                except Exception as e:
                    Hooks.input_manager["S"] = False
                    print(f"Error: {e}")
                    return

                self.draw.render_path()
                self.draw.entry_and_exit()
                self.draw.present()
                self.window.render_image()

            if Hooks.input_manager["P"] and self.done_solve:
                try:
                    if self.path_show:
                        Hooks.input_manager["P"] = False
                        self.draw.render_path()
                        self.draw.entry_and_exit()
                        self.draw.present()
                        self.window.render_image()
                        self.path_show = False
                    elif not self.path_show:
                        Hooks.input_manager["P"] = False
                        self.draw.buff_3d[:] = self.buff_cache
                        self.draw.present()
                        self.window.render_image()
                        self.path_show = True
                except Exception as e:
                    Hooks.input_manager["P"] = False
                    print(f"Error: {e}")

            if Hooks.input_manager["C"] and self.done_gen:
                Hooks.input_manager["C"] = False
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

            if Hooks.input_manager["UP"]:
                self.draw.camera_y -= self.draw.speed
                self.draw.present()
                self.window.render_image()

            if Hooks.input_manager["DOWN"]:
                self.draw.camera_y += self.draw.speed
                self.draw.present()
                self.window.render_image()

            if Hooks.input_manager["LEFT"]:
                self.draw.camera_x -= self.draw.speed
                self.draw.present()
                self.window.render_image()

            if Hooks.input_manager["RIGHT"]:
                self.draw.camera_x += self.draw.speed
                self.draw.present()
                self.window.render_image()

            if Hooks.input_manager["E"]:
                if not self.done_solve:
                    print("Error: Maze not generated or solved yet")
                elif self.done_solve:
                    MazeManager.write_maze(
                        self.configs["output_file"],
                        self.draw.maze_hex,
                        self.configs["entry"],
                        self.configs["exit"],
                        self.draw.path
                    )
                Hooks.input_manager["E"] = False


        except (KeyboardInterrupt, EOFError):
            self.window.exit_window(None)
        except Exception as e:
            print(f"Error: {e}")
