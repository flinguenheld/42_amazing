from maze_generator.maze import Maze
from maze_generator.config import Config
from maze_generator.walker import Walker
from maze_generator.path_finder import PathFinder


from typing import Optional, Set
import random
from datetime import datetime
import time

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
            # TODO: Implement defaults straight in Config
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

    @staticmethod
    def destroy_walls(maze: Maze, full_path: Set[tuple[int, int]]):
        """
        - Receives a Maze object and a set of all cells coordinates
        - Iterates through all visited cells
        - Breaks random wall if not near a 0 cell/nor creating a 0 cell
        - Yield Maze at each wall broken
        """
        for cur_r, cur_c in full_path:
            if not (
                0 > cur_r > maze.nb_row - 2
                and 0 > cur_c > maze.nb_col - 2
                and maze.values[cur_r][cur_c] != 0
            ):
                pass
            try:
                if random.randint(0, 1) != 1:
                    raise ValueError
                for y in range(-1, 1):
                    for x in range(-1, 1):
                        if (
                            0 >= cur_r - y >= maze.nb_row - 1
                            and 0 >= cur_c - x >= maze.nb_col - 1
                            and (cur_r - y, cur_c - x) not in maze.cells_42
                            and maze.values[cur_r - y][cur_c - x] == 0b0000
                        ):
                            raise ValueError
                neighbours = {
                    (cur_r - r, cur_c - c) for r, c in maze.WALL_MAP.keys()
                }
                ngbr = random.choice([i for i in neighbours if i in full_path])
                maze.break_wall((cur_r, cur_c), ngbr, True)
                yield maze
            except ValueError:
                pass

    def generate(self) -> Maze | None:
        """
        - Returns last yield Maze from generator()
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
        if self.config.get("seed") is None:
            random.seed(
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}{time.time()}"
            )
        else:
            random.seed(self.config.get("seed"))

        maze = Maze(
            self.config.nb_row,
            self.config.nb_col,
            self.config.entry,
            self.config.exit,
            self.config.perfect,
        )

        full_path: Set[tuple[int, int]] = set()
        not_visited = {
            (r, c)
            for r in range(maze.nb_row)
            for c in range(maze.nb_col)
            if (r, c) not in maze.cells_42
        }

        yield maze

        path = Walker(maze, False, maze.start, maze.end).walk()
        full_path.update(path)
        not_visited.difference_update(path)

        yield maze

        while len(not_visited) != 0:
            choice = random.choice(list(not_visited))
            path = Walker(maze, False, choice, full_path).walk()
            full_path.update(path)
            not_visited.difference_update(path)
            print(self.config.get("nb_col"))

            yield maze

        if maze.perfect is False:
            for wmaze in MazeGenerator.destroy_walls(maze, full_path):
                yield wmaze
                maze = wmaze

        maze.set_solution(PathFinder(maze, self.config).search())

        yield maze
