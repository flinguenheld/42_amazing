from typing import List, Tuple
from Maze import Maze
import random
import time


class MazeGenerator:
    def __init__(self, maze: Maze) -> None:
        """
        - Stores maze related values (width, height, start, end)
        - Initializes self.path for self.first_trail
        """
        self.maze = maze
        self.max = (maze.nb_row - 1, maze.nb_col - 1)
        self.begin = maze.start
        self.goal = maze.end
        self.path: List[Tuple[int, int]] = [self.begin]

    def __go_back(self) -> None:
        """
        - Find first neighbouring in-path cell
        - Erase path from index of found cell
        """
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        cur_r, cur_c = self.path[-1]
        index = len(self.path) - 1

        if 0 < cur_r < self.max[0] and 0 < cur_c < self.max[1]:
            for r, c in moves:
                if (cur_r + r, cur_c + c) in self.path:
                    new_index = [
                        k
                        for k, v in enumerate(self.path)
                        if v == (cur_r + r, cur_c + c)
                    ][0]
                    if new_index < index:
                        index = new_index
        else:
            index = 2
        if index < 2:
            index = 2

        self.path = self.path[:index]

    def __get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        - Try every move possible from cell
        - Only keep those who are within bound
        - Return those as list
        """
        cur_r, cur_c = self.path[-1]
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        valid_moves = []
        new_r, new_c = 0, 0

        for dir_r, dir_c in moves:
            new_r = cur_r + dir_r
            new_c = cur_c + dir_c
            if 0 <= new_r <= self.max[0] and 0 <= new_c <= self.max[1]:
                valid_moves.append((new_r, new_c))

        return valid_moves

    def __not_in_path(
        self, valid_moves: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        - Takes list from self.get_valid_moves
        - Returns those who don't give to an in-path cell
                                                    -as a list
        """
        return [i for i in valid_moves if (i[0], i[1]) not in self.path]

    def other_trails(self) -> None:
        """
        - All trails after the first one
        - Choose a random cell that is done already in the maze
        - Walk from cell to maze
        - Write path to maze.values
        """
        tab = [
            (r, c)
            for c in range(self.maze.nb_col)
            for r in range(self.maze.nb_row)
        ]
        labyrinth = [(r, c) for (r, c) in tab if self.maze.values[r][c] != 0xF]
        cur_r, cur_c = random.choice(
            self.__not_in_path([t for t in tab if t not in labyrinth])
        )
        self.path = [(cur_r, cur_c)]
        while self.path[-1] not in labyrinth:
            valid_moves = self.__not_in_path(self.__get_valid_moves())

            if len(valid_moves) == 0:
                self.__go_back()
            else:
                choice = random.choice(valid_moves)
                self.path.append((choice[0], choice[1]))

        self.__update_maze()

    def first_trail(self) -> None:
        """
        - First walk of the maze
        - Goes from start to end / entry to exit
        - Writes path to maze.values on return
        """
        while self.path[-1] != self.goal:
            valid_moves = self.__not_in_path(self.__get_valid_moves())

            if len(valid_moves) == 0:
                self.__go_back()
            else:
                choice = random.choice(valid_moves)
                self.path.append((choice[0], choice[1]))

        self.__update_maze()

    def __get_cell_value(self, i: int, r: int, c: int) -> int:
        """
        - Look at preceding cell
        - Remove appropriate wall
        - Look at next cell
        - Remove appropriate wall
        """
        value = 0xF

        if i > 0 + 1:
            if self.path[i - 1] == (r - 1, c):
                value -= 1
            elif self.path[i - 1] == (r + 1, c):
                value -= 4
            elif self.path[i - 1] == (r, c - 1):
                value -= 8
            elif self.path[i - 1] == (r, c + 1):
                value -= 2

        if i < len(self.path) - 1:
            if self.path[i + 1] == (r - 1, c):
                value -= 1
            elif self.path[i + 1] == (r + 1, c):
                value -= 4
            elif self.path[i + 1] == (r, c - 1):
                value -= 8
            elif self.path[i + 1] == (r, c + 1):
                value -= 2

        return value

    def __update_maze(self) -> None:
        """
        - Writes data from self.path to self.maze.values
        """
        for i, (r, c) in enumerate(self.path):
            self.maze.values[r][c] = self.__get_cell_value(i, r, c)

        print(self.maze)
        time.sleep(0.05)

    def generate(self) -> None:

        self.first_trail()
        while (
            len(
                [
                    (r, c)
                    for c in range(self.maze.nb_col)
                    for r in range(self.maze.nb_row)
                    if self.maze.values[r][c] == 0xF
                ]
            )
            > (self.maze.nb_row * self.maze.nb_col) / 10
        ):
            self.other_trails()
