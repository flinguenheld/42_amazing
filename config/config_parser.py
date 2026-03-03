from typing import Annotated, Tuple
from pydantic import BaseModel, Field

SIZE_MIN = 5
SIZE_MAX = 100


class blahblah:
    def aaaaa(self):
        print("ssss")


class ConfigParser(BaseModel):
    width: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="WIDTH")]
    height: Annotated[int, Field(ge=SIZE_MIN, le=SIZE_MAX, alias="HEIGHT")]
    entry: Annotated[Tuple[int, int], Field(alias="ENTRY")]
    exit: Annotated[Tuple[int, int], Field(alias="EXIT")]
    output_file: Annotated[
        str, Field(min_length=3, max_length=30, alias="OUTPUT_FILE")
    ]
    perfect: Annotated[bool, Field(alias="PERFECT")]

    # @classmethod
    def my_ass(cls):
        print("my arse")

    # @classmethod
    # def model_validate():
    #     pass
