from mazegen.maze import Maze

from mazegen.walker import Walker
from mazegen.path import Path

from typing import Generator, List, Set
from abc import ABC, abstractmethod
import random


class Algorithm(ABC):
    MOVES = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )

    def __init__(self, maze: Maze, rand: random.Random) -> None:
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
        pass

    def _get_neighbours(self, cell: tuple[int, int]) -> List[tuple[int, int]]:
        neighbours: List[tuple[int, int]] = list()
        for move in self.MOVES:
            new = (cell[0] + move[0], cell[1] + move[1])
            if (
                0 <= new[0] < self._maze.nb_row
                and 0 <= new[1] < self._maze.nb_col
            ):
                neighbours.append(new)
        return neighbours


class Wilson(Algorithm):
    def __init__(self, maze: Maze, rand: random.Random) -> None:
        super().__init__(maze, rand)
        self.__full_path: Set[tuple[int, int]] = set()

    def solve(self) -> Generator[Maze, None, None]:
        self.__find_first_path()
        yield self._maze

        while self._not_visited:
            self.__find_next_path()
            yield self._maze

    def __find_first_path(self) -> Maze:
        path = Walker(self._maze, self._maze.start, self._maze.end).walk(
            self._rand
        )
        self.__full_path.update(path)
        self._not_visited.difference_update(path)

    def __find_next_path(self) -> Maze:
        choice = self._rand.choice(sorted(list(self._not_visited)))

        path = Walker(self._maze, choice, self.__full_path).walk(self._rand)
        if self._maze.perfect is False and len(path) > 3:
            self.__create_loop(path)
        self.__full_path.update(path)
        self._not_visited.difference_update(path)

    def __create_loop(self, path: Path) -> None:
        first_cell_neighbours = [
            i
            for i in self._get_neighbours(path[0])
            if i not in path
            and i in self.__full_path
            and self._maze.values[i[0]][i[1]] in {0xE, 0xD, 0xB, 0x7}
        ]
        if len(first_cell_neighbours) > 0:
            target = self._rand.choice(first_cell_neighbours)
            self._maze.break_wall(path[0], target, safe=True)


class DFS(Algorithm):
    def __init__(self, maze: Maze, rand: random.Random) -> None:
        super().__init__(maze, rand)
        start = rand.choice(sorted(list(self._not_visited)))
        self.__visited = [start]
        self._not_visited.remove(start)

    def _get_neighbours(self, cell: tuple[int, int]) -> List[tuple[int, int]]:
        neighbours = super()._get_neighbours(cell)
        return [i for i in neighbours if i in self._not_visited]

    def solve(self) -> None:
        while self.__visited:
            cur = self.__visited.pop()
            neighbours = self._get_neighbours(cur)
            if neighbours:
                target = self._rand.choice(neighbours)
                self.__visited.append(cur)
                self._maze.break_wall(cur, target, safe=False)
                self.__visited.append(target)
                self._not_visited.remove(target)
                yield self._maze
