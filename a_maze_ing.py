import sys
from termcolor import cprint
from controller import Controller
from pydantic import ValidationError


def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"


def main():

    try:
        if len(sys.argv) != 2:
            raise FileNotFoundError

        controller = Controller(sys.argv[1])
        controller.load_config()

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
