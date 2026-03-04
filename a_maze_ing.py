import sys
from Controller import Controller


def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"


def main():
    controller = Controller(sys.argv[1])
    controller.init_maze()


if __name__ == "__main__":
    main()
