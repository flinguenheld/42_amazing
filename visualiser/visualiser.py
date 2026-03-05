from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Footer, Header, Digits, Button
from textual.app import App, ComposeResult
from textual import events


class TimeDisplay(Digits):
    """Blah"""


class Stopwatch(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00:00")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.add_class("started")
        elif event.button.id == "stop":
            self.remove_class("started")


class Visualiser(App):
    CSS_PATH = "style_tuto.tcss"
    BINDINGS = [("t", "next_theme", "Next theme")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch())

    # #########################################################################
    # ############################################################ THEMES #####
    def on_mount(self) -> None:
        self.action_next_theme()

    # def on_key(self, event: events.Key) -> None:
    #     if event.key.isdecimal():
    #         self.action_next_theme()

    def action_next_theme(self) -> None:
        """Change theme"""

        match self.theme[-5:]:
            case "uvbox":
                self.theme = "catppuccin-latte"
            case "latte":
                self.theme = "catppuccin-macchiato"
            case "hiato":
                self.theme = "catppuccin-mocha"
            case "mocha":
                self.theme = "catppuccin-frappe"
            case _:
                self.theme = "gruvbox"


if __name__ == "__main__":
    app = Visualiser()
    app.run()
