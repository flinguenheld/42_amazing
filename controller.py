from typing import Optional
from maze import Maze
from config.config_parser import ConfigParser
from visualiser.visualiser import Visualiser


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░▀█▀░█▀▄░█▀█░█░░░█░░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░░█░░█▀▄░█░█░█░░░█░░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
class Controller:
    def __init__(self, config_path: str) -> None:
        self.config_path: str = config_path

        # TODO: USE PROPERTIES ? ##############################################
        self.maze: Optional[Maze] = None
        self.__visualiser: Optional[Visualiser] = None

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
        # print(self.__maze)
        self.__visualiser = Visualiser(self.maze)

    def run_visualiser(self) -> None:
        self.__visualiser.run()
