from config.config_parser import ConfigParser
import sys
from termcolor import cprint
from visualiser.visualiser import Visualiser
from mazegen.config import Config
from pydantic import ValidationError


def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise FileNotFoundError

        parser = ConfigParser(sys.argv[1])
        parsed = parser.parse_file()
        config = Config.model_validate(parsed)
        if config.get("nb_row") <= 9 or config.get("nb_col") <= 9:
            cprint(
                "Size too small, omitting 42 logo",
                file=sys.stderr,
                color="red",
            )

        application = Visualiser(config=config)
        application.run()

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


if __name__ == "__main__":
    main()
