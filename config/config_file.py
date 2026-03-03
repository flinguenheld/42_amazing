from .config_parser import ConfigParser
from typing import Tuple


class ConfigFile:
    def __init__(self, file_name: str):
        self.__file_name = file_name

    @staticmethod
    def parse_line(line: str, dictionary: dict[str, str | Tuple[str, str]]):
        if not line.startswith("#"):
            key, value = line.split("=")

            if "," in value:
                left, right = value.strip().split(",")
                dictionary[key] = (left, right)
            else:
                dictionary[key] = value.strip()

    def parse_file(self) -> dict[str, int | bool | str | Tuple[int, int]]:
        parsed_values = {}
        with open(self.__file_name, "r") as f:
            for line in f.readlines():
                ConfigFile.parse_line(line, parsed_values)

        parser = ConfigParser.model_validate(parsed_values)
        return ConfigParser.model_dump(parser)


if __name__ == "__main__":
    cfg = ConfigFile("config.txt")
    my_dict = cfg.parse_file()
    print("hello")
    print(my_dict)
