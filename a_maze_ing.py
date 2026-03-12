from config.config_parser import ConfigParser
import sys
from termcolor import cprint
from visualiser.visualiser import Visualiser


def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"


def main():
    try:
        if len(sys.argv) != 2:
            raise FileNotFoundError

        parser = ConfigParser(sys.argv[1])
        config = parser.parse_file()

        application = Visualiser(config=config)
        application.run()

    #   except ValidationError as e:
    #       cprint("Config file error", file=sys.stderr, color="red")
    #       for err in e.errors():
    #           cprint(f"  - {err['msg']}", file=sys.stderr, color="red")
    #       cprint(usage(), file=sys.stderr, color="yellow")

    except FileNotFoundError:
        cprint("Config file not found", file=sys.stderr, color="red")
        cprint(usage(), file=sys.stderr, color="yellow")


#   except Exception as e:
#       cprint(e, file=sys.stderr, color="red")
#       cprint(usage(), file=sys.stderr, color="yellow")


if __name__ == "__main__":
    main()
