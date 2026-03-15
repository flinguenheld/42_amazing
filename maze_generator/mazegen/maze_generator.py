from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.path_finder import PathFinder

from mazegen.algorithms import Algorithm
from typing import Optional
import random


class MazeGenerator:
    """
    - Standalone class that fully handles the instantiation/filling
            of a Maze based on a Config object passed on initialization.
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """- Chooses between passed as arg/default Config object"""
        if config is not None:
            self.config = config
        else:
            self.config = Config()

    def __reset_attributes(self) -> Maze:
        self.__rand = random.Random(self.config.get("seed"))

        self.__maze = Maze(
            self.config.nb_row,
            self.config.nb_col,
            self.config.entry,
            self.config.exit,
            self.config.perfect,
            self.config.seed,
            self.config.loop_ratio
        )

    def __solve_maze(self) -> Maze:
        self.__maze.set_solution(PathFinder(self.__maze, self.config).search())
        return self.__maze

    def generate(self):
        self.__reset_attributes()
        yield self.__maze

        algo = [
            i
            for i in Algorithm.__subclasses__()
            if self.config.get("algo") in str(i)
        ][0]
        for maze in algo(self.__maze, self.__rand).solve():
            yield maze

        self.__solve_maze()
        yield self.__maze

    def get_maze(self) -> Maze:
        """
        - Skips to last Maze yield by generate()
        """
        return list(self.generate())[-1]
