from typing import Optional, Dict
from maze_generator.maze import Maze
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
        self.cfg: Optional[Dict[str, int | bool | str | None]] = None

    def load_config(self) -> None:
        parser = ConfigParser(self.config_path)
        self.cfg = parser.parse_file()

    def set_maze(self, maze: Maze) -> None:
        self.maze = maze

    def run_visualiser(self) -> None:
        self.__visualiser = Visualiser(self.maze)
        self.__visualiser.refresh_maze()
        self.__visualiser.run()
