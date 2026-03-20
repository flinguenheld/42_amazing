from typing import Tuple, Callable, List

from mazegen.maze import Maze
from mazegen.path_finder import PathFinder
import asyncio


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█░░░█░█░▀█▀░▀█▀░█▀█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀█░█░█░█░░░█░█░░█░░░█░░█░█░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀
class Solution:
    def __init__(self, drawing_function: Callable):
        self._drawing_function = drawing_function
        self._points: List[tuple[int, int]] = []
        self._animation_on = True

    def is_active(self) -> List[tuple[int, int]]:
        return self._points

    # ########################################################################
    # ############################################################# CYCLE ####
    async def cycle(self, maze: Maze, start: Tuple[int, int]) -> None:
        self._animation_on = True

        # Up points --
        self._points = PathFinder(maze, start).search().get_list()

        # Run --
        # if self.is_active():
        for index in range(0, len(self._points), 1):
            if not self._animation_on:
                break

            group = self._points[index : index + 2]
            if len(group) == 2:
                self._draw(group[0], group[1], "error")
                await asyncio.sleep(0.02)

    # ########################################################################
    # ############################################################# CLEAN ####
    def stop_animation(self):
        self._animation_on = False

    # ########################################################################
    # ############################################################# CLEAN ####
    def clean_up_to(self, to: Tuple[int, int]) -> None:
        if to in self._points:
            for index in range(0, len(self._points), 1):
                if self._points[index] == to:
                    break
                group = self._points[index : index + 2]
                if len(group) == 2:
                    self._draw(group[0], group[1])

    # ########################################################################
    # ############################################################## DRAW ####
    def _draw(
        self,
        point_from: Tuple[int, int],
        point_to: Tuple[int, int],
        colour: str = "primary",
    ) -> None:
        self._drawing_function(
            point_from[1],
            point_from[0],
            point_to[1],
            point_to[0],
            colour,
        )

    # ########################################################################
    # ######################################################## DEACTIVATE ####
    def deactivate(self, clean: bool) -> None:
        if clean and self.is_active():
            self.clean_up_to(self._points[-1])

        self._points.clear()
