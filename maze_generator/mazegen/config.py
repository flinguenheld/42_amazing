from mazegen.algorithms import Algorithm

from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

SIZE_MIN = 2
SIZE_MAX = 1000

# TODO: Find a way to make default exit (nb_row - 1, nb_col - 1)


class Config(BaseModel):
    """
    - Class that stores config related info, runnnig Field() checks
                                                at each assignation
    - Provides safe ways to get and set attributes
    """

    nb_col: Annotated[
        Optional[int],
        Field(default=15, ge=SIZE_MIN, le=SIZE_MAX, alias="WIDTH"),
    ]
    nb_row: Annotated[
        Optional[int],
        Field(default=15, ge=SIZE_MIN, le=SIZE_MAX, alias="HEIGHT"),
    ]
    entry: Annotated[
        Optional[tuple[int, int]], Field(default=(0, 0), alias="ENTRY")
    ]
    exit: Annotated[
        Optional[tuple[int, int]], Field(default=(14, 14), alias="EXIT")
    ]
    output_file: Annotated[
        Optional[str],
        Field(
            default="maze.txt",
            min_length=3,
            max_length=30,
            alias="OUTPUT_FILE",
        ),
    ]
    perfect: Annotated[Optional[bool], Field(default=False, alias="PERFECT")]
    seed: Annotated[
        Optional[Any],
        Field(default=None, alias="SEED"),
    ]
    algo: Annotated[Optional[str], Field(default="Wilson", alias="ALGO")]
    loop_ratio: Annotated[
        Optional[int], Field(default=100, ge=0, le=100, alias="LOOP_RATIO")
    ]

    # Enable passing new value of modified attributes into checks before write
    class Config:
        """Configures BaseModel behaviour"""

        validate_assignment = True

    @field_validator("entry", "exit")
    @classmethod
    def is_coor_in_maze(cls, value: tuple[int, int]) -> tuple[int, int]:
        """Checks entry and exit coordinates are greater than 0"""
        row, col = value
        if row < 0 or col < 0:
            raise ValueError("Coordinates have to be higher than 0")
        return value

    @model_validator(mode="after")
    def are_in_the_maze(self) -> Any:
        """Checks entry and exit are inside the maze limits"""
        entry_row, entry_col = self.entry
        exit_row, exit_col = self.exit

        if entry_row >= self.nb_row:
            raise ValueError(f"Entry Y can't be higher than {self.nb_row}")
        if exit_row >= self.nb_row:
            raise ValueError(f"Exit Y can't be higher than {self.nb_row}")

        if entry_col >= self.nb_col:
            raise ValueError(f"Entry X can't be higher than {self.nb_col}")
        if exit_col >= self.nb_col:
            raise ValueError(f"Exit X can't be higher than {self.nb_col}")

        return self

    @model_validator(mode="after")
    def entry_exit_cant_be_equal(self) -> Any:
        """Checks entry and exit are not equal"""
        if self.entry == self.exit:
            raise ValueError("Entry and Exit can't be equal")

        return self

    @model_validator(mode="after")
    def algorithm_is_valid(self) -> Any:
        """Checks algorithm is implemented as children of class Algorithm"""
        for child in Algorithm.__subclasses__():
            if self.algo in str(child):
                return self
        raise ValueError(f"{self.algo} is not a valid algorithm")

    def set(self, param_name: str, new_value: Any) -> None:
        """
        - Sets attribute passed as a string to new value (after runs checks)
        """
        setattr(self, param_name, new_value)

    def get(self, param_name: str) -> Any:
        """
        - Gets attribute passed as a string, defaults to None if not found
        """
        return getattr(self, param_name, None)
