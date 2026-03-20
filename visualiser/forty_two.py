import random
import asyncio
from typing import Tuple, Set, Callable, List


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀█▀░█░█░░░▀█▀░█░█░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█░█░█▀▄░░█░░░█░░░░░█░░█▄█░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀░▀░░▀░░░▀░░░░░▀░░▀░▀░▀▀▀
class FortyTwo:
    """Allows TMaze to enlight the 42 in the middle of maze"""

    def __init__(self, drawing_function: Callable) -> None:
        self._drawing_function = drawing_function
        self._points: List[tuple[int, int]] = []
        self._colours = [
            "secondary",
            "accent",
            "foreground",
            "success",
            "warning",
            "error",
            "surface",
            "panel",
        ]

    def deactivate(self) -> None:
        for row, col in self._points:
            self._drawing_function(row, col, "background")
        self._points = []

    def update_points(self, points: Set[Tuple[int, int]]) -> None:
        self._points = list(points)

    async def cycle(self) -> None:
        if self._points:
            for _ in range(1, random.randint(3, 6)):
                await self._colour_them(random.choice(self._colours))
            await self._colour_them("background")

    async def _colour_them(self, colour: str) -> None:
        if self._points:
            random.shuffle(self._points)
            for row, col in self._points:
                self._drawing_function(row, col, colour)
                await asyncio.sleep(0.02)
