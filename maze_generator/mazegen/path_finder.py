from mazegen.maze import Maze
from mazegen.path import Path

from typing import Dict, Tuple, List, Optional
from collections import deque


class PathFinder:
    """Class using BFS to find quickest path between maze.entry
    or passed start and maze.exit"""

    def __init__(self, maze: Maze, start: Optional[int] = None) -> None:
        self.__start = maze.entry if start is None else start
        self.__maze: Maze = maze
        self.__tab: Dict[Tuple[int, int], Tuple[int, int]] = dict()
        self.__queue = deque([self.__start])

    @staticmethod
    def get_valid_moves(val: int) -> List[Tuple[int, int]]:
        """Find out which direction we can go in from current cell's value

        - Return:
            possible moves as list
        """
        moves = list()
        b = f"{val:04b}"
        walls = [char == "0" for char in b]
        if walls[0] is True:
            moves.append((0, -1))
        if walls[1] is True:
            moves.append((1, 0))
        if walls[2] is True:
            moves.append((0, 1))
        if walls[3] is True:
            moves.append((-1, 0))
        return moves

    def search(self) -> Path:
        """Go from current cell to first accessible neighbour repeatedly
                                until current cell has no accessible
                                neighbours, go back to last cell who has
                                accessible unvisited neighbours
        - Return:
            Path object if foundpath
            None otherwise
        """
        while self.__queue:
            cur = self.__queue.popleft()
            if cur == self.__maze.exit:
                return self.backtrack()
            val = self.__maze.values[cur[0]][cur[1]]
            for move in self.get_valid_moves(val):
                new_r, new_c = (cur[0] + move[0], cur[1] + move[1])
                if (new_r, new_c) not in self.__tab:
                    self.__tab[(new_r, new_c)] = cur
                    self.__queue.append((new_r, new_c))
        return Path([])

    def backtrack(self) -> Path:
        """Follow trail from end to start to reconstruct coordinates list"""
        cur = self.__maze.exit
        path = Path([self.__maze.exit])
        while cur != self.__start:
            cur = self.__tab[cur]
            path.append(cur)
        path.path.reverse()
        return path
