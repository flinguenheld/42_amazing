from .config_model import ConfigModel


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▀░░░█▀█░█▀█░█▀▄░█▀▀░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░█▀▀░░█░░█░█░░░█▀▀░█▀█░█▀▄░▀▀█░█▀▀░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀░░░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀
class ConfigParser:
    def __init__(self, file_name: str):
        self.__file_name = file_name

    @staticmethod
    def __parse_line(line: str, dictionary: dict[str, str | tuple[str, str]]):
        """
        - Split the line in two with =
        - Split again with , if necessary
        - Save the pair in the given dictionary
        """
        if not line.startswith("#"):
            key, value = line.split("=")

            if "," in value:
                col, row = value.strip().split(",")
                dictionary[key] = (row, col)
            else:
                dictionary[key] = value.strip()

    def parse_file(self) -> dict[str, int | bool | str | tuple[int, int]]:
        """
        - Open the config file
        - Parse each line to feed a model
        - Return a dictionary with all config options

        Raise Value error if forbidden, missing or invalid data
        """
        parsed_values = {}
        with open(self.__file_name, "r") as f:
            for line in f.readlines():
                ConfigParser.__parse_line(line, parsed_values)

        parser = ConfigModel.model_validate(parsed_values)
        return ConfigModel.model_dump(parser)
