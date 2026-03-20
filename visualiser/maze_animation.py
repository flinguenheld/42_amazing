import asyncio
from typing import Optional, Callable, Generator

from mazegen.maze import Maze
from mazegen.maze_generator import MazeGenerator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░▀▀█░█▀▀░░░█▀█░█▀█░▀█▀░█▄█░█▀█░▀█▀░▀█▀░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀█░▄▀░░█▀▀░░░█▀█░█░█░░█░░█░█░█▀█░░█░░░█░░█░█░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░▀░▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀
class MazeAnimation:
    """
    Allows TMaze create and move forward an iterator
    to build the maze step by step
    """

    def __init__(
        self, maze_generator: MazeGenerator, drawing_function: Callable
    ):
        self._drawing_function = drawing_function
        self._maze_generator = maze_generator
        self._iterator: Generator[Maze, None, None] | None = None
        self._maze: Optional[Maze] = None

    def is_active(self) -> bool:
        return self._iterator is not None

    def get_last_maze(self) -> Optional[Maze]:
        return self._maze

    def start_new_animation(self) -> None:
        self._iterator = self._maze_generator.generate()

    async def cycle(self) -> None:
        while self.next_step():
            await asyncio.sleep(0)

    def next_step(self) -> bool:
        if self._iterator:
            maze = next(self._iterator, None)
            if maze:
                self._drawing_function(maze)
                self._maze = maze
                return True
            else:
                self._iterator = None

        return False
