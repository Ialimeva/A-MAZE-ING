class Keymap:
    ESC = 65307

    @classmethod
    def get(cls, key: str) -> int | str:
        return getattr(cls, key.upper(), "Unknown key")