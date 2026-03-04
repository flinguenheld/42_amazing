from maze import Maze
from config.config_parser import ConfigParser


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░▀█▀░█▀▄░█▀█░█░░░█░░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░░█░░█▀▄░█░█░█░░░█░░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class Controller:
    def __init__(self, config_path: str) -> None:
        self.config_path: str = config_path
        self.maze: Maze = None

    def load_config(self):
        cfg = ConfigParser(self.config_path)
        conf = cfg.parse_file()
        self.maze = Maze(
            nb_row=conf["nb_row"],
            nb_col=conf["nb_col"],
            entry=conf["entry"],
            exit=conf["exit"],
            perfect=conf["perfect"],
        )
        print(self.maze)
