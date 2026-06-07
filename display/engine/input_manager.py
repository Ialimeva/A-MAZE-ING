"""Input event handling module.

This module defines keyboard event hooks used by the application.
It maintains a shared input state and updates key flags in response
to key press and key release events.
"""

from typing import Any
from .keymap import Keymap


class Hooks():
    """Keyboard input event manager.

    This class provides static callback methods for handling keyboard
    events and maintaining the current input state. Key states are
    stored in the shared ``input_manager`` dictionary and can be
    queried by other application components.

    Attributes:
        input_manager: Mapping of supported input actions
            to their current pressed state.
    """

    input_manager: dict[str, bool] = {
        "SPACE": False,
        "ESC": False,
        "ENTER": False,
        "S": False,
        "P": False,
        "G": False,
        "C": False,
        "E": False,
        "UP": False,
        "DOWN": False,
        "LEFT": False,
        "RIGHT": False,
    }

    @staticmethod
    def key_pressed(keycode: int, param: Any) -> None:
        """Handle a key press event.

        Updates the input state by marking the corresponding key action
        as active.

        Args:
            keycode: Numeric key code received from the windowing
                system.
            param: Additional callback data supplied by the
                windowing system. This parameter is not used.
        """
        if keycode == Keymap.get("space"):
            Hooks.input_manager["SPACE"] = True

        if keycode == Keymap.get("esc"):
            Hooks.input_manager["ESC"] = True

        if keycode == Keymap.get("enter"):
            Hooks.input_manager["ENTER"] = True

        if keycode == Keymap.get("s"):
            Hooks.input_manager["S"] = True

        if keycode == Keymap.get("p"):
            Hooks.input_manager["P"] = True

        if keycode == Keymap.get("g"):
            Hooks.input_manager["G"] = True

        if keycode == Keymap.get("c"):
            Hooks.input_manager["C"] = True

        if keycode == Keymap.get("e"):
            Hooks.input_manager["E"] = True

        if keycode == Keymap.get("up"):
            Hooks.input_manager["UP"] = True

        if keycode == Keymap.get("down"):
            Hooks.input_manager["DOWN"] = True

        if keycode == Keymap.get("left"):
            Hooks.input_manager["LEFT"] = True

        if keycode == Keymap.get("right"):
            Hooks.input_manager["RIGHT"] = True

    @staticmethod
    def key_released(keycode: int, param: Any) -> None:
        """Handle a key release event.

        Updates the input state by marking the corresponding key action
        as inactive.

        Args:
            keycode: Numeric key code received from the windowing
                system.
            param: Additional callback data supplied by the
                windowing system. This parameter is not used.
        """
        if keycode == Keymap.get("esc"):
            Hooks.input_manager["ESC"] = False

        if keycode == Keymap.get("up"):
            Hooks.input_manager["UP"] = False

        if keycode == Keymap.get("down"):
            Hooks.input_manager["DOWN"] = False

        if keycode == Keymap.get("left"):
            Hooks.input_manager["LEFT"] = False

        if keycode == Keymap.get("right"):
            Hooks.input_manager["RIGHT"] = False
