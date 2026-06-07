"""Game controller module.

This module defines the Game class, which coordinates maze generation,
rendering, user input handling, maze solving, and exporting results.
It serves as the main application controller between the rendering
engine, window system, and maze management logic.
"""

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

import random
import signal
from typing import Any, Generator
from .engine.window import Window
from .engine.input_manager import Hooks
from .renderer.renderer import Draw
from .display_config import DisplayConfig
from core import MazeManager
from mazegen import Maze


class Game:
    """Main game controller.

    This class manages the application lifecycle, including maze
    generation, rendering, solving, user interaction, and exporting
    maze solutions. It acts as the central coordinator between the
    window system, renderer, input manager, and maze algorithms.

    Attributes:
        configs: Configuration dictionary containing the program settings.
        display_config: Display configuration object.
        window: Window instance.
        img_data: Source Tileset Image used for rendering.
        buff_data: Internal rendering buffer.
        display_data: Display buffer presented to the window.
        draw: Renderer responsible for drawing maze elements.
        maze: Current maze instance.
        gen: Maze generation generator.
        buff_cache: Cached rendering buffer used for restoring maze state.
        is_starting: Indicates whether generation has started.
        show_menu: Indicates whether the menu is visible.
        path_show: Indicates whether the solution path is hidden.
        regen_maze: Indicates whether maze regeneration is active.
        done_gen: Indicates whether maze generation is complete.
        done_solve: Indicates whether maze solving is complete.
        change_wcolor: Indicates whether wall colors changed.
        solve: Maze solving generator.
    """

    def __init__(self, configs: dict[str, Any]) -> None:
        """Initialize the game controller.

        Creates the display system, rendering pipeline, maze generation
        components, and application state variables.

        Args:
            configs: Configuration dictionary containing
                the program settings.
        """
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

        self.is_starting = False
        self.show_menu = False
        self.path_show = False
        self.regen_maze = False
        self.done_gen = False
        self.done_solve = False
        self.change_wcolor = False
        self.solve: Generator[
            tuple[int, int], None, list[tuple[int, int]]
        ]
        self.draw.path = []
        signal.signal(signal.SIGINT, self.sig_handler)

    def sig_handler(self, signum: int, frame: Any) -> None:
        """Handle operating system interrupt signals.

        Ensures the application exits gracefully when an interrupt signal
        is received.

        Args:
            signum: Signal number received by the process.
            frame: Current execution frame.
        """
        self.window.exit_window(None)

    def run(self) -> None:
        """Start the game application.

        Displays the welcome screen and starts the window event loop.
        """
        self.window.welcome_page()
        self.window.start(self.update)

    def generate_step(
            self,
            generator: Generator[Maze, None, None],
            key: str
    ) -> None:
        """Advance maze generation by one step.

        Retrieves the next maze state from the generator, updates the
        renderer, and refreshes the display. When generation completes,
        initializes the maze solver generator.

        Args:
            generator: Maze generation generator producing
                intermediate maze states.
            key: Input key associated with the generation action.
        """
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
        """Process user input and update application state.

        Handles keyboard actions for maze generation, regeneration,
        solving, camera movement, menu display, wall color changes,
        path visibility toggling, exporting, and application shutdown.

        Args:
            _ (Any): Callback parameter supplied by the window system.
                The value is unused.
        """
        try:
            if Hooks.input_manager["ESC"]:
                self.is_starting = False
                self.window.exit_window(None)
                Hooks.input_manager["ESC"] = False

            if Hooks.input_manager["ENTER"]:
                self.is_starting = True
                self.generate_step(self.gen, "ENTER")

            if Hooks.input_manager["SPACE"] and self.is_starting:
                Hooks.input_manager["SPACE"] = False
                if not self.show_menu:
                    self.show_menu = True
                    self.window.put_menu()
                else:
                    self.show_menu = False
                    self.draw.present()
                    self.window.render_image()

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
            return
        except Exception as e:
            print(f"Error: {e}")
            return
