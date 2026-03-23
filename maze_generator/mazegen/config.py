from mazegen.algorithms import Algorithm

from typing import Annotated, Any, Optional, Tuple, ClassVar, List
from pydantic import BaseModel, Field, field_validator, model_validator
from random import Random
from datetime import datetime
import time


class Config(BaseModel):
    """Class that checks and stores parameters used for maze generation

    - Public attributes:

        nb_col: int, number of columnns
        nb_row: int, number of rows

        entry: tuple[int, int], maze entry coordinates
        exit: tuple[int, int], maze exit coordinates

        output_file: str, file to write maze's __str__() to

        perfect: bool, perfect character of maze
                (only one path between any (Ax, Ay) and (Bx, By))
        seed: Any, data used to seed random.Random instance
                                    used throuhought generation
        algo: str, algorithm used for generation ("DFS" or "Wilson")
        loop_ratio: int, between 0 and 100, proportion of
                                    broken walls if perfect = False


        nb_col and nb_row must be positive integers between 2 and 1000

        entry and exit must be composed of positive integers
                smaller than nb_col - 1 or nb_row - 1 and cannot be equal
    """

    MIN_SIZE: ClassVar[int] = 5
    MAX_SIZE: ClassVar[int] = 200

    nb_col: Annotated[int, Field(ge=MIN_SIZE, le=MAX_SIZE, alias="WIDTH")]
    nb_row: Annotated[int, Field(ge=MIN_SIZE, le=MAX_SIZE, alias="HEIGHT")]
    entry: Annotated[Tuple[int, int], Field(alias="ENTRY")]
    exit: Annotated[Tuple[int, int], Field(alias="EXIT")]
    output_file: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            alias="OUTPUT_FILE",
        ),
    ]
    perfect: Annotated[bool, Field(default=False, alias="PERFECT")]
    seed: Annotated[
        Optional[Any],
        Field(alias="SEED"),
    ] = None
    algo: Annotated[str, Field(alias="ALGO")] = "Wilson"
    loop_ratio: Annotated[int, Field(ge=0, le=100, alias="LOOP_RATIO")] = 100
    print_to_file: Annotated[bool, Field(alias="PRINT_TO_FILE")] = True

    past_seeds: List[Any] = list()

    class Config:
        """Configure BaseModel behaviour"""

        # Enable passing new value into checks before assignation
        validate_assignment = True

    @field_validator("entry", "exit")
    @classmethod
    def is_coor_in_maze(cls, value: tuple[int, int]) -> tuple[int, int]:
        """Check entry and exit coordinates are greater than 0"""
        row, col = value
        if row < 0 or col < 0:
            raise ValueError("Coordinates have to be higher than 0")
        return value

    @model_validator(mode="after")
    def are_in_the_maze(self) -> Any:
        """Checks entry and exit are inside the maze limits"""
        (entry_row, entry_col) = self.entry
        (exit_row, exit_col) = self.exit

        if entry_row >= self.nb_row or entry_col >= self.nb_col:
            raise ValueError(
                f"Entry ({entry_col}, {entry_row}) has to be"
                f" inside the maze ({self.nb_col}, {self.nb_row}))"
            )
        if exit_row >= self.nb_row or exit_col >= self.nb_col:
            raise ValueError(
                f"Exit ({exit_col}, {exit_row}) has to be"
                f" inside the maze ({self.nb_col}, {self.nb_row}))"
            )
        return self

    @model_validator(mode="after")
    def entry_exit_cant_be_equal(self) -> Any:
        """Check entry and exit are not equal"""
        if self.entry == self.exit:
            raise ValueError("Entry and Exit can't be equal")

        return self

    @model_validator(mode="after")
    def algorithm_is_valid(self) -> Any:
        """Check algorithm is implemented as children of class Algorithm"""
        for child in Algorithm.__subclasses__():
            if self.algo == str(child).split(".")[-1].strip(">'"):
                return self
        raise ValueError(f"{self.algo} is not a valid algorithm")

    def update_seed(self, seed: Optional[Any] = None) -> None:
        """Sets seed to argument or generated"""
        if seed:
            try:
                Random(seed)
            except Exception:
                pass
            else:
                if seed not in self.past_seeds:
                    self.past_seeds.append(self.seed)
                self.seed = seed
        elif (
            self.past_seeds
            and self.seed == self.past_seeds[-1]
            and (self.seed is None or "AUTO" in self.seed)
        ):
            self.seed = (
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}AUTO{time.time()}"
            )
            self.past_seeds.append(self.seed)

    def set(self, param_name: str, new_value: Any) -> None:
        """Set attribute passed as a string to new value (after runs checks)"""
        setattr(self, param_name, new_value)

    def get(self, param_name: str) -> Any:
        """Gets attribute passed as a string, defaults to None if not found"""
        return getattr(self, param_name, None)
