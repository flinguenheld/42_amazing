from typing import Dict, Tuple, List
from Maze import Maze
from config.config_parser import ConfigParser
from termcolor import cprint
from pydantic import ValidationError
import sys

def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"

class Controller:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.maze = None

    def load_config(self) -> Dict[str, str | int | bool | Tuple[int, int]] | None:
        try:
            if len(sys.argv) != 2:
                raise FileNotFoundError

            cfg = ConfigParser(sys.argv[1])
            config = cfg.parse_file()
            return config

        except ValidationError as e:
           cprint("Config file error", file=sys.stderr, color="red")
           for err in e.errors():
               cprint(f"  - {err['msg']}", file=sys.stderr, color="red")
           cprint(usage(), file=sys.stderr, color="yellow")

        except FileNotFoundError:
            cprint("Config file not found", file=sys.stderr, color="red")
            cprint(usage(), file=sys.stderr, color="yellow")
 
        except Exception as e:
            cprint(e, file=sys.stderr, color="red")
            cprint(usage(), file=sys.stderr, color="yellow")
        return None

    def init_maze(self) -> None:
        conf = self.load_config()
        self.maze = Maze(conf['nb_row'], conf['nb_col'],
                         conf['entry'], conf['exit'],
                         conf['perfect'])
        print(self.maze)
