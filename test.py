from config.config_parser import ConfigParser
from mazegen.config import Config
from mazegen.maze_generator import MazeGenerator
import time
import subprocess


def main() -> None:
    parser = ConfigParser("config_test.txt")
    parsed = parser.parse_file()
    config = Config.model_validate(parsed)

    generator = MazeGenerator(config)
    for maze in generator.generate():
        if maze.start == (99, 99):
            with open("maze.txt", "w") as fd:
                fd.write(str(maze))
                print(maze)
                breakpoint()


if __name__ == "__main__":
    main()
