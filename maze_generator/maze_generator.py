from maze_generator.maze import Maze
from maze_generator.config import Config
from maze_generator.walker import Walker
from maze_generator.path_finder import PathFinder


from typing import Optional, Set
import random

# TODO: Build installable via pip package (uv build, .whl)


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
                if self.__rand.randint(0, 1) != 1:
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

        self.__full_path: Set[tuple[int, int]] = set()
        self.__not_visited = {
            (r, c)
            for r in range(self.__maze.nb_row)
            for c in range(self.__maze.nb_col)
            if (r, c) not in self.__maze.cells_42
        }

        return self.__maze

    def __find_first_path(self) -> Maze:
        path = Walker(
            self.__maze, False, self.__maze.start, self.__maze.end
        ).walk(self.__rand)
        self.__full_path.update(path)
        self.__not_visited.difference_update(path)

    def __find_next_path(self) -> Maze:
        choice = self.__rand.choice(sorted(list(self.__not_visited)))
        path = Walker(self.__maze, False, choice, self.__full_path).walk(
            self.__rand
        )
        self.__full_path.update(path)
        self.__not_visited.difference_update(path)

    def __solve_maze(self) -> Maze:
        self.__maze.set_solution(PathFinder(self.__maze, self.config).search())
        return self.__maze

    def generate(self, animate: Optional[bool] = False):
        """
        - Instantiate Maze with config set in __init__()
            - yield empty maze
        - Instantiate and use Walkers to fill maze branch by branch
                with new paths until no cell is left unvisited
            - yield maze after each walker
        - Destroy walls if maze must not be perfect
            - yield wall at each wall broken
        - Find quickest path from entry to exit and write solution to maze
        - yield last maze
        """
        self.__reset_attributes()
        if animate:
            yield self.__maze

        self.__find_first_path()
        if animate:
            yield self.__maze

        while len(self.__not_visited) != 0:
            self.__find_next_path()
            yield self.__maze

        if self.__maze.perfect is False:
            for maze in self.__destroy_walls():
                if animate:
                    yield maze

        self.__solve_maze()
        yield self.__maze
