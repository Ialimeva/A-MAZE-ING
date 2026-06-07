"""Keyboard key mapping module.

This module defines key code constants used throughout the application
and provides a utility method for retrieving key codes by name.
"""


class Keymap:
    """Keyboard key code definitions.

    This class stores key codes recognized by the application and
    provides a lookup method for converting key names into their
    corresponding numeric key codes.

    The key codes are intended to be used by the input handling system
    when processing keyboard events.
    """

    SPACE = 0x20
    ESC = 0xFF1B
    ENTER = 0xFF0D
    S = 0x73
    P = 0x70
    G = 0x67
    C = 0x63
    E = 0x65
    UP = 0xff52
    DOWN = 0xff54
    LEFT = 0xff51
    RIGHT = 0xff53

    @classmethod
    def get(cls, key: str) -> int | str:
        """Retrieve a key code by name.

        Args:
            key: Name of the key to retrieve. The lookup is
                case-insensitive.

        Returns:
            int | str: The corresponding key code if the key exists,
            otherwise ``"Unknown key"``.
        """
        return getattr(cls, key.upper(), "Unknown key")
