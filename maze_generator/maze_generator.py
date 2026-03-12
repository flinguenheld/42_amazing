from maze_generator.maze import Maze
from maze_generator.config_model import ConfigModel
from maze_generator.walker import Walker
from maze_generator.path import FullPath
from maze_generator.path_finder import PathFinder


from typing import Dict
import random

# TODO: Add '42' to the middle of the maze when possible
# TODO: Write docstrings for all functions
# TODO: Instantiate maze inside MazeGenerator and return it on generate()

class MazeGenerator:
    """
    - Standalone class that fully handles the creation/generation
            of a maze based on a config dict passed on instanciation.
    - Uses Wilson's algorithm with LERW for generation
    """

    def __init__(self, cfg: Dict) -> None:
        """
        - Check passed config through ConfigModel to ensure data sanity
        - Create base maze with retrieved parameters
        """
        parser = ConfigModel.model_validate(cfg)
        self.config = ConfigModel.model_dump(parser)
        self.maze = Maze(
            self.config["nb_row"],
            self.config["nb_col"],
            self.config["entry"],
            self.config["exit"],
            self.config["perfect"],
        )

        self.fp = FullPath()
        self.not_visited = {
            (r, c)
            for r in range(self.maze.nb_row)
            for c in range(self.maze.nb_col)
            if (r, c) not in self.maze.cells_42
        }
        random.seed(4)

    def destroy_walls(self) -> None:
        """
        - Iterate through all visited cells
        - Breaks random wall if not near a 0 cell/nor creating a 0 cell
        """
        for cur_r, cur_c in self.fp.get_set():
            if not (
                0 > cur_r > self.maze.nb_row - 2
                and 0 > cur_c > self.maze.nb_col - 2
                and self.maze.values[cur_r][cur_c] != 0
            ):
                pass
            try:
                if random.randint(0, 1) != 1:
                    raise ValueError
                for y in range(-1, 1):
                    for x in range(-1, 1):
                        if (
                            0 >= cur_r - y >= self.maze.nb_row - 1
                            and 0 >= cur_c - x >= self.maze.nb_col - 1
                            and (cur_r - y, cur_c - x)
                            not in self.maze.cells_42
                            and self.maze.values[cur_r - y][cur_c - x]
                            == 0b0000
                        ):
                            raise ValueError
                neighbours = [
                    (cur_r - r, cur_c - c)
                    for r, c in self.maze.WALL_MAP.keys()
                ]
                ngbr = random.choice(
                    [i for i in neighbours if i in self.fp.get_set()]
                )
                self.maze.break_wall((cur_r, cur_c), ngbr, True)
            except ValueError:
                pass

    def generate(self) -> Maze:
        """
        - Instantiate and use Walkers to fill maze branch by branch
                with new paths until no cell is unvisited
        - Destroy walls if maze must not be perfect
        - Return maze
        """
        walker = Walker(self.maze, True, self.maze.start, self.maze.end)
        for coor in self.fp.append(walker.walk()):
            self.not_visited.discard(coor)

        while len(self.not_visited) != 0:
            choice = random.choice(list(self.not_visited))
            walker = Walker(self.maze, False, choice, self.fp.get_set())
            for coor in self.fp.append(walker.walk()):
                self.not_visited.discard(coor)
        if self.maze.perfect is False:
            self.destroy_walls()
        for cell in self.fp.get_set():
            if cell in self.maze.cells_42:
                self.maze.values[cell[0]][cell[1]] = 0xF
        self.maze.set_solution(PathFinder(self.maze, self.config).search())
        print(self.maze.solution.path)
        return self.maze
