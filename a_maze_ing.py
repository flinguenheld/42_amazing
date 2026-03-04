import sys
from Controller import Controller
from maze_generator import MazeGenerator


def usage() -> str:
    return f"\nUsage: {sys.argv[0]} CONFIG_FILE"


def main():
    controller = Controller(sys.argv[1])
    controller.init_maze()
    generator = MazeGenerator(controller.maze)
    generator.first_trail()



if __name__ == "__main__":
    main()
