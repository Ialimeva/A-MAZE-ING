from core import ConfigManager, MazeExporter
from mazegen import MazeGenerator
from display import Game, maze_config
import sys

def main() -> None:
    if len(sys.argv) != 2:
        print("Error arguments")
        sys.exit(1)

    try:
        filename: str = sys.argv[1]
        manager: ConfigManager = ConfigManager(filename)
        configs: dict = manager.get_config()
        maze_config["colums"] = configs["width"]
        maze_config["rows"] = configs["height"]
        game = Game()
        game.run()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()