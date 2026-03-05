from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator, model_validator

# TODO: MANAGE MIN MAX HERE ??
# TODO: manage 42 in the middle
SIZE_MIN = 2
SIZE_MAX = 500




# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░░█▄█░█▀█░█▀▄░█▀▀░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░░█░█░█░█░█░█░█▀▀░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀
class ConfigModel(BaseModel):
    nb_col: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="WIDTH")]
    nb_row: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="HEIGHT")]
    entry: Annotated[tuple[int, int], Field(alias="ENTRY")]
    exit: Annotated[tuple[int, int], Field(alias="EXIT")]
    output_file: Annotated[
        str, Field(min_length=3, max_length=30, alias="OUTPUT_FILE")
    ]
    perfect: Annotated[bool, Field(alias="PERFECT")]

    # #########################################################################
    # ########               ⡇⢸ ⢀⣀ ⡇ ⠄ ⢀⣸ ⢀⣀ ⣰⡀ ⢀⡀ ⡀⣀ ⢀⣀               ########
    # ########               ⠸⠃ ⠣⠼ ⠣ ⠇ ⠣⠼ ⠣⠼ ⠘⠤ ⠣⠜ ⠏  ⠭⠕               ########

    # #########################################################################
    # ###################### ENTRY & EXIT VALUES HAVE TO BE HIGHER THAN 0 #####
    @field_validator("entry", "exit")
    @classmethod
    def does_id_start_with_m(cls, value: tuple[int, int]) -> tuple[int, int]:
        row, col = value
        if row < 0 or col < 0:
            raise ValueError("Coordinates have to be higher than 0")
        return value

    # #########################################################################
    # ############################### ENTRY & EXIT HAVE TO BE IN THE MAZE #####
    @model_validator(mode="after")
    def are_in_the_maze(self) -> Any:

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

    # #########################################################################
    # ################################# ENTRY & EXIT HAVE TO BE DIFFERENT #####
    @model_validator(mode="after")
    def entry_exit_cant_be_equal(self) -> Any:

        if self.entry == self.exit:
            raise ValueError("Entry and Exit can't be equal")

        return self
