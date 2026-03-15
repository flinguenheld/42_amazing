from textual.app import RenderResult
from textual.widgets import Static


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░░░█░░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀
class TTitle(Static):
    def __init__(self) -> None:
        super().__init__(classes="ttitles")
        self.__to_print = """
▄████▄       ██▄  ▄██ ▄████▄ ██████ ██████       ██ ███  ██  ▄████  
██▄▄██       ██ ▀▀ ██ ██▄▄██  ▄▄▀▀  ██▄▄         ██ ██ ▀▄██ ██  ▄▄▄ 
██  ██ ▄▄▄▄▄ ██    ██ ██  ██ ██████ ██▄▄▄▄ ▄▄▄▄▄ ██ ██   ██  ▀███▀  
            """

    def render(self) -> RenderResult:
        return self.__to_print


class TTitleOption(Static):
    def __init__(self) -> None:
        super().__init__(classes="ttitles")
        self.__to_print = """
▄████▄ █████▄ ██████ ██ ▄████▄ ███  ██ ▄█████ 
██  ██ ██▄▄█▀   ██   ██ ██  ██ ██ ▀▄██ ▀▀▀▄▄▄ 
▀████▀ ██       ██   ██ ▀████▀ ██   ██ █████▀ 
            """

    def render(self) -> RenderResult:
        return self.__to_print
