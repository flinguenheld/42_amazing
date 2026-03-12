from maze_generator.maze import Maze
from maze_generator.config import Config
from maze_generator.path import Path

from typing import Dict, Tuple, List
from collections import deque


class PathFinder:
    """
    - Class generating a list of lists of tuples,
            representing path of coordinates for every
            possible solution for the maze, sorted by length
    """

    def __init__(self, maze: Maze, config: Config) -> None:
        self.maze: Maze = maze
        self.maze.start = config.entry
        self.maze.end = config.exit
        self.tab: Dict[Tuple[int, int], Tuple[int, int]] = dict()
        self.queue = deque([self.maze.start])

    @staticmethod
    def get_valid_moves(val: int) -> List[Tuple[int, int]]:
        moves = list()
        b = f"{val:04b}"
        walls = [char == '0' for char in b]
        if walls[0] is True:
            moves.append((0, -1))
        if walls[1] is True:
            moves.append((1, 0))
        if walls[2] is True:
            moves.append((0, 1))
        if walls[3] is True:
            moves.append((-1, 0))
        return moves

    def search(self) -> Path | None:
        while self.queue:
            cur = self.queue.popleft()
            if cur == self.maze.end:
                return self.backtrack()
            val = self.maze.values[cur[0]][cur[1]]
            for move in self.get_valid_moves(val):
                new_r, new_c = (cur[0] + move[0], cur[1] + move[1])
                if (new_r, new_c) not in self.tab:
                    self.tab[(new_r, new_c)] = cur
                    self.queue.append((new_r, new_c))
        return None

    def backtrack(self) -> Path:
        cur = self.maze.end
        path = Path([self.maze.end])
        while cur != self.maze.start:
            cur = self.tab[cur]
            path.append(cur)
        path.path.reverse()
        return path
