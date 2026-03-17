from typing import Tuple
from mazegen.maze import Maze


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░░░█▀█░█░█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░░░█▀█░░█░░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀
class Player:
    def __init__(self, maze: Maze):
        self._maze = maze
        self.reset()

    def reset(self):
        self._row = self._maze.start[0]
        self._col = self._maze.start[1]
        self._previous_position = self._maze.start
        self._counter = 0

    # ########################################################################
    # ############################################################# MOVE #####
    def move(self, key: str):

        cell_hexa = self._maze.values[self._row][self._col]
        self._previous_position = (self._row, self._col)

        match key:
            case "up":
                if cell_hexa & 0b0001 != 0b0001:  # Top
                    self._counter += 1
                    self._row -= 1
            case "down":
                if cell_hexa & 0b0100 != 0b0100:  # Bottom
                    self._counter += 1
                    self._row += 1
            case "right":
                if cell_hexa & 0b0010 != 0b0010:  # Right
                    self._counter += 1
                    self._col += 1
            case "left":
                if cell_hexa & 0b1000 != 0b1000:  # Left
                    self._counter += 1
                    self._col -= 1

    # ########################################################################
    # ######################################################## ACCESSORS #####
    def is_winning(self) -> bool:
        return self.get_position() == self._maze.end

    def get_position(self) -> Tuple[int, int]:
        return (self._row, self._col)

    def get_previous_position(self) -> Tuple[int, int]:
        return self._previous_position

    def get_counter(self) -> Tuple[int, int]:
        return (self._counter, len(self._maze.solution))
