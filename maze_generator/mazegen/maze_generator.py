from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.path_finder import PathFinder

from mazegen.algorithms import Algorithm
from typing import Optional, Generator
import random


class MazeGenerator:
    """Class handling the whole process of generating a Maze

    - Public attributes:
        self.config: Config object passed on instanciation or generated
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """Sets public config to either passed as argument or default"""
        if config is not None:
            self.config = config
        else:
            self.config = Config()

    def init_maze(self) -> None:
        """Resets maze with config info"""
        self.__maze = Maze(
            self.config.get("nb_row"),
            self.config.get("nb_col"),
            self.config.get("entry"),
            self.config.get("exit"),
            self.config.get("perfect"),
            self.config.get("seed"),
            self.config.get("loop_ratio"),
        )
        if self.__maze.start in self.__maze.cells_42:
            self.__maze.start = [
                i
                for i in Algorithm._get_neighbours(
                    self.__maze, self.__maze.start
                )
                if i not in self.__maze.cells_42
            ][0]
        if self.__maze.end in self.__maze.cells_42:
            self.__maze.start = [
                i
                for i in Algorithm._get_neighbours(
                    self.__maze, self.__maze.end
                )
                if i not in self.__maze.cells_42
            ][0]

    def __reset_attributes(self) -> None:
        """Set/update private attributes before generation"""
        self.__rand = random.Random(self.config.get("seed"))
        self.init_maze()

    def __solve_maze(self) -> Maze:
        """Write PathFinder's result into maze.solution

        - Return:
            maze
        """
        self.__maze.set_solution(PathFinder(self.__maze, self.config).search())
        return self.__maze

    def generate(self) -> Generator[Maze, None, None]:
        """Clear maze, choose and execute algorithm, solve maze

        - Yield:
            maze at every step
        """
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
        if self.config.get("output_file"):
            with open(self.config.get("output_file"), "w") as fd:
                fd.write(str(maze))
        yield self.__maze

    def get_maze(self) -> Maze:
        """Skip to last maze of generate() and return it"""
        return list(self.generate())[-1]
