from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

SIZE_MIN = 2
SIZE_MAX = 1000


class Config(BaseModel):
    nb_col: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="WIDTH")]
    nb_row: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="HEIGHT")]
    entry: Annotated[tuple[int, int], Field(alias="ENTRY")]
    exit: Annotated[tuple[int, int], Field(alias="EXIT")]
    output_file: Annotated[
        str, Field(min_length=3, max_length=30, alias="OUTPUT_FILE")
    ]
    perfect: Annotated[bool, Field(alias="PERFECT")]
    seed: Annotated[
        Optional[Any],
        Field(default=None, alias="SEED"),
    ]

    # Enable passing new value of modified attributes into checks before write
    class Config:
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

    def set(self, param_name: str, new_value: Any) -> None:
        setattr(self, param_name, new_value)

    def get(self, param_name: str) -> Any:
        return getattr(self, param_name, None)
