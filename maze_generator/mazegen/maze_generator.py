from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.path_finder import PathFinder

from mazegen.algorithms import Algorithm
from typing import Optional
import random

# TODO: Rework destroy_walls()


class MazeGenerator:
    """
    - Standalone class that fully handles the instantiation/filling
            of a Maze based on a Config object passed on initialization.
    - Uses Wilson's algorithm with LERW for maze generation
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """- Chooses between passed as arg/default Config object"""
        if config is not None:
            self.config = config
        else:
            self.config = Config()

    def __destroy_walls(self):
        """
        - Receives a Maze object and a set of all cells coordinates
        - Iterates through all visited cells
        - Breaks random wall if not near a 0 cell/nor creating a 0 cell
        - Yield Maze at each wall broken
        """
        for cur_r, cur_c in self.__full_path:
            if not (
                0 > cur_r > self.__maze.nb_row - 2
                and 0 > cur_c > self.__maze.nb_col - 2
                and self.__maze.values[cur_r][cur_c] != 0
            ):
                pass
            try:
                if self.__rand.randint(0, 2) != 1:
                    raise ValueError
                for y in range(-1, 1):
                    for x in range(-1, 1):
                        if (
                            0 >= cur_r - y >= self.__maze.nb_row - 1
                            and 0 >= cur_c - x >= self.__maze.nb_col - 1
                            and (cur_r - y, cur_c - x)
                            not in self.__maze.cells_42
                            and self.__maze.values[cur_r - y][cur_c - x]
                            == 0b0000
                        ):
                            raise ValueError
                neighbours = {
                    (cur_r - r, cur_c - c)
                    for r, c in self.__maze.WALL_MAP.keys()
                }
                ngbr = self.__rand.choice(
                    [i for i in neighbours if i in self.__full_path]
                )
                self.__maze.break_wall((cur_r, cur_c), ngbr, True)
                yield self.__maze
            except ValueError:
                pass

    def __reset_attributes(self) -> Maze:
        self.__rand = random.Random(self.config.get("seed"))

        self.__maze = Maze(
            self.config.nb_row,
            self.config.nb_col,
            self.config.entry,
            self.config.exit,
            self.config.perfect,
            self.config.seed,
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
