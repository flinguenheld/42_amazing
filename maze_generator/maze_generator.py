from maze_generator.maze import Maze
from maze_generator.config_model import ConfigModel
from maze_generator.walker import Walker
from maze_generator.path import FullPath

from typing import Dict
import random

# TODO: Add '42' to the middle of the maze when possible
# TODO: Write docstrings for all functions
# TODO: Instantiate maze inside MazeGenerator and return it on generate()


class MazeGenerator:
    def __init__(self, cfg: Dict) -> None:
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
        # random.seed(4)

    def destroy_walls(self) -> None:
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

    def generate(self) -> None:
        walker = Walker(self.maze, True, self.maze.start, self.maze.end)
        for coor in self.fp.append(walker.walk()):
            self.not_visited.discard(coor)
        self.print_maze()

        while len(self.not_visited) != 0:
            choice = random.choice(list(self.not_visited))
            walker = Walker(self.maze, False, choice, self.fp.get_set())
            for coor in self.fp.append(walker.walk()):
                self.not_visited.discard(coor)
            self.print_maze()
        if self.maze.perfect is False:
            self.destroy_walls()
        for cell in self.fp.get_set():
            if cell in self.maze.cells_42:
                self.maze.values[cell[0]][cell[1]] = 0xF
        self.print_maze()
        return self.maze

        # TESTING RELATED CODE
        # CALL TO self.print_maze() AND DEF

    def print_maze(self) -> None:
        for line in self.maze.values:
            for char in line:
                print(f"{char:x}" if char != 0xF else "_", end="")
            print()
        print("\n\n")
