from mazegen.maze import Maze

from mazegen.walker import Walker

from typing import Generator, List, Set
from abc import ABC, abstractmethod
import random


class Algorithm(ABC):
    """Parent class for all implemented algorithms

    - Public attributes:
        MOVES: tuple[tuple[int, int]], coordinate evolution for
                                            one step in any direction

    - Attributes accessible to children:
        Set in __init__():
         - Args
            maze: Maze object passed by MazeGenerator
            rand: rand object passed by MazeGenerator

        _maze
        _rand
        _not_visited: Set[tuple[int, int]], all cells not yet visited
                                                        and not in logo
    """

    MOVES = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )

    def __init__(self, maze: Maze, rand: random.Random) -> None:
        """Corrects maze's start or exit if they are in logo"""
        self._maze = maze
        self._rand = rand
        self._not_visited: Set[tuple[int, int]] = {
            (r, c)
            for r in range(self._maze.nb_row)
            for c in range(self._maze.nb_col)
            if (r, c) not in self._maze.cells_42
        }

    @abstractmethod
    def solve(self) -> Generator[Maze, None, None]:
        """Abstract method to be implemented by each algorithm"""
        pass

    @staticmethod
    def _get_neighbours(
        maze: Maze, cell: tuple[int, int]
    ) -> List[tuple[int, int]]:
        """Get neighbouring cells within maze

        - Args:
            maze: Maze object, current maze state
            cell: tuple[int, int], coordinate of cell which neighbours
                                                        are to be returned
        - Returns
            list[tuple[int, int]] of cells in MOVES offset
                                        from arg and within maze limits
        """
        neighbours: List[tuple[int, int]] = list()
        for move in Algorithm.MOVES:
            new = (cell[0] + move[0], cell[1] + move[1])
            if 0 <= new[0] < maze.nb_row and 0 <= new[1] < maze.nb_col:
                neighbours.append(new)
        return neighbours

    def _create_loops(self) -> Generator[Maze, None, None]:
        """Iterate through all 'dead-end' cell in the maze (3 walls)
                                    and leave only two parallel walls
        - Yield:
            maze at each broken wall
        """
        dead_ends = {0xE, 0xD, 0xB, 0x7}

        targets = [
            (r, c)
            for c in range(1, self._maze.nb_col - 1)
            for r in range(1, self._maze.nb_row - 1)
            if self._maze.values[r][c] in dead_ends
            and self._rand.randint(0, 100) in range(0, self._maze.loop_ratio)
        ]
        for r, c in targets:
            target = (r, c)
            value = self._maze.values[r][c]
            match value:
                case 0xE:
                    target = (r + 1, c)
                case 0xD:
                    target = (r, c - 1)
                case 0xB:
                    target = (r - 1, c)
                case 0x7:
                    target = (r, c + 1)
            if target not in self._maze.cells_42:
                self._maze.break_wall((r, c), target, safe=False)
            if target in targets:
                targets.remove(target)
            yield self._maze


class Wilson(Algorithm):
    """Algorithm that uses LERW to create a perfect maze

    - Public attributes:
        see Algorithm class
    """

    def __init__(self, maze: Maze, rand: random.Random) -> None:
        """Initialise set of all visited coordinates"""
        super().__init__(maze, rand)
        if self._maze.cells_42:
            mid_r, mid_c = (
                int((self._maze.nb_row - 1) / 2),
                int((self._maze.nb_col - 1) / 2),
            )
            self.__first_start = (mid_r - 1, mid_c + 2)
            self.__first_end = (mid_r + 1, mid_c + 2)
        else:
            self.__first_start = self._maze.entry
            self.__first_end = self._maze.exit
        self.__full_path: Set[tuple[int, int]] = set()

    def solve(self) -> Generator[Maze, None, None]:
        """Find arbitraty first path, then all random others,
                                        then create loops if needed
        - Yield:
            maze at every step
        """

        self.__find_first_path()
        yield self._maze

        while self._not_visited:
            self.__find_next_path()
            yield self._maze

        if not self._maze.perfect:
            for maze in self._create_loops():
                yield maze

    def __find_first_path(self) -> None:
        """Use Walker's LERW to find first path from maze's entry to exit"""
        path = Walker(self._maze, self.__first_start, self.__first_end).walk(
            self._rand
        )
        self.__full_path.update(path.get_list())
        self._not_visited.difference_update(path.get_list())

    def __find_next_path(self) -> None:
        """Use Walker's LERW to find any but first path from random to maze"""
        choice = self._rand.choice(sorted(list(self._not_visited)))

        path = Walker(self._maze, choice, self.__full_path).walk(self._rand)
        self.__full_path.update(path.get_list())
        self._not_visited.difference_update(path.get_list())


class DFS(Algorithm):
    """Algorithm using DFS to generate a perfect maze

    - Public attributes:
        see Algorithm class
    """

    def __init__(self, maze: Maze, rand: random.Random) -> None:
        """Choose starting position and initialize visited cells list"""
        super().__init__(maze, rand)
        start = rand.choice(sorted(list(self._not_visited)))
        self.__visited = [start]
        self._not_visited.remove(start)

    def _get_unvisited_neighbours(
        self, cell: tuple[int, int]
    ) -> List[tuple[int, int]]:
        """Add condition 'don't be visited' to parent's implementation"""
        neighbours = super()._get_neighbours(self._maze, cell)
        return [i for i in neighbours if i in self._not_visited]

    def solve(self) -> Generator[Maze, None, None]:
        """Jump from current cell to first neighbour until current cell
                        has no neighbours, then go back to first cell that
                        has unvisited neighbours and go again
        - Yield:
            maze at every step
        """
        while self.__visited:
            cur = self.__visited.pop()
            neighbours = self._get_unvisited_neighbours(cur)
            if neighbours:
                target = self._rand.choice(neighbours)
                self.__visited.append(cur)
                self._maze.break_wall(cur, target, safe=False)
                self.__visited.append(target)
                self._not_visited.remove(target)
                yield self._maze

        if not self._maze.perfect:
            for maze in self._create_loops():
                yield maze
