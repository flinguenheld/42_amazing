import time
from maze_generator.maze import Maze
from maze_generator.config import Config
from maze_generator.walker import Walker
from maze_generator.path_finder import PathFinder


from typing import Optional, Set
from datetime import datetime
import time
import random


class MazeGenerator:
    """
    - Standalone class that fully handles the instantiation/filling
            of a Maze based on a Config object passed on initialization.
    - Uses Wilson's algorithm with LERW for maze generation
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        """
        - Chooses between passed as arg/default Config object
        - Seeds random()
        """
        if config:
            self.config = config
        else:
            self.config = Config.model_validate(
                {
                    "WIDTH": 10,
                    "HEIGHT": 10,
                    "ENTRY": (0, 0),
                    "EXIT": (9, 9),
                    "OUTPUT_FILE": "dummy.txt",
                    "PERFECT": True,
                }
            )
        self.full_path: Set[tuple[int, int]] = set()

    def destroy_walls(self) -> None:
        """
        - Iterates through all visited cells
        - Breaks random wall if not near a 0 cell/nor creating a 0 cell
        - Yield maze at each wall broken
        """
        for cur_r, cur_c in self.full_path:
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
                    [i for i in neighbours if i in self.full_path]
                )
                self.maze.break_wall((cur_r, cur_c), ngbr, True)
                yield self.maze
            except ValueError:
                pass

    def generate(self) -> Maze | None:
        """
        - Wrapper for generator animate(), skips to last yield maze
        """
        return list(self.animate())[-1]

    def animate(self):
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
        if not self.config.get("seed"):
            random.seed(
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}{time.time()}"
            )
        else:
            random.seed(self.config.get("seed"))

        self.maze = Maze(
            self.config.nb_row,
            self.config.nb_col,
            self.config.entry,
            self.config.exit,
            self.config.perfect,
        )

        not_visited = {
            (r, c)
            for r in range(self.maze.nb_row)
            for c in range(self.maze.nb_col)
            if (r, c) not in self.maze.cells_42
        }

        yield self.maze

        walker = Walker(self.maze, True, self.maze.start, self.maze.end)
        for coor in walker.walk():
            self.full_path.add(coor)
            not_visited.discard(coor)

        yield self.maze

        while len(not_visited) != 0:
            choice = random.choice(list(not_visited))
            walker = Walker(self.maze, False, choice, self.full_path)
            for coor in walker.walk():
                self.full_path.add(coor)
                not_visited.discard(coor)

            yield self.maze

        if self.maze.perfect is False:
            for maze in self.destroy_walls():
                yield maze

        self.maze.set_solution(PathFinder(self.maze, self.config).search())

        yield self.maze
