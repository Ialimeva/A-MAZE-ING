class Keymap:
    ESC = 65307
    ENTER = 65293

    @classmethod
    def get(cls, key: str) -> int | str:
        return getattr(cls, key.upper(), "Unknown key")