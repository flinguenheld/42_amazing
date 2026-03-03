from typing import Annotated, Tuple, Any
from pydantic import BaseModel, Field, field_validator, model_validator

SIZE_MIN = 2
SIZE_MAX = 500


# TODO: manage 42 in the middle


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░░█▄█░█▀█░█▀▄░█▀▀░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░░█░█░█░█░█░█░█▀▀░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀
class ConfigModel(BaseModel):
    width: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="WIDTH")]
    height: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="HEIGHT")]
    entry: Annotated[Tuple[int, int], Field(alias="ENTRY")]
    exit: Annotated[Tuple[int, int], Field(alias="EXIT")]
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
    def does_id_start_with_m(cls, value: Tuple[int, int]) -> Tuple[int, int]:
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

        if entry_row > self.height:
            raise ValueError(f"Entry Y can't be higher than {self.height}")
        if exit_row > self.height:
            raise ValueError(f"Exit Y can't be higher than {self.height}")

        if entry_col > self.width:
            raise ValueError(f"Entry X can't be higher than {self.width}")
        if exit_col > self.width:
            raise ValueError(f"Exit X can't be higher than {self.width}")

        return self
