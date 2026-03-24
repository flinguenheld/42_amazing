from mazegen.maze import Maze
from mazegen.config import Config
from mazegen.path_finder import PathFinder
from mazegen.algorithms import Algorithm

from typing import Optional, Generator, Any, Dict
import random


class MazeGenerator:
    """Class handling the whole process of generating a Maze

    - Public attributes:
        self.config: Config object passed on instantiation or generated
    """

    def __init__(
        self,
        config_dict: Optional[Dict[str, Any]] = None,
        config: Optional[Config] = None,
    ) -> None:
        """Sets public config to either passed as argument or default"""
        if config and isinstance(config, Config):
            self.config = config
        elif config_dict and isinstance(config_dict, dict):
            self.config = Config.model_validate(config_dict)
        else:
            self.config = Config.model_validate(
                {
                    "WIDTH": 20,
                    "HEIGHT": 20,
                    "ENTRY": (0, 0),
                    "EXIT": (19, 19),
                    "PERFECT": False,
                    "OUTPUT_FILE": "maze.txt",
                }
            )

    def init_maze(self) -> None:
        """Reset maze with config info"""
        self.config.update_seed()
        self.__maze = Maze(
            self.config.get("nb_row"),
            self.config.get("nb_col"),
            self.config.get("entry"),
            self.config.get("exit"),
            self.config.get("perfect"),
            self.config.get("seed"),
            self.config.get("loop_ratio"),
        )
        if self.__maze.entry in self.__maze.cells_42:
            self.__maze.entry = [
                i
                for i in Algorithm._get_neighbours(
                    self.__maze, self.__maze.entry
                )
                if i not in self.__maze.cells_42
            ][0]
        if self.__maze.exit in self.__maze.cells_42:
            self.__maze.exit = [
                i
                for i in Algorithm._get_neighbours(
                    self.__maze, self.__maze.exit
                )
                if i not in self.__maze.cells_42
            ][0]

    def __reset_attributes(self) -> None:
        """Set/update private attributes before generation"""
        self.__rand = random.Random(self.config.get("seed"))
        self.init_maze()

    def generate(self) -> Generator[Maze, None, None]:
        """Clear maze, choose and execute algorithm, solve maze

        - Yield:
            maze at every step
        """
        self.__reset_attributes()
        yield self.__maze

        algo: Any = [
            i
            for i in Algorithm.__subclasses__()
            if self.config.get("algo") == str(i).split(".")[-1].strip(">'")
        ][0]
        for maze in algo(self.__maze, self.__rand).solve():
            yield maze

        self.__maze.set_solution(PathFinder(self.__maze).search())

        if self.config.get("print_to_file"):
            with open(self.config.get("output_file"), "w") as fd:
                fd.write(str(maze))
        yield self.__maze

    def get_maze(self) -> Maze:
        """Skip to last maze of generate() and return it"""
        return list(self.generate())[-1]
