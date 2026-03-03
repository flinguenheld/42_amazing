from typing import Annotated, Tuple
from pydantic import BaseModel, Field

SIZE_MIN = 2
SIZE_MAX = 500


# manage 42 in the middle


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
