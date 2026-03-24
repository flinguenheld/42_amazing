from mazegen import MazeGenerator

if __name__ == "__main__":
    """ Short test script to prove reusability of the code """

    # Instantiate and use a generator with a default config
    generator = MazeGenerator()
    maze = generator.get_maze()
    print(maze)
    print(maze.solution)
    print(maze.seed)
    print("\n\n")

    # Instantiate and use a generator with a custom Dict
    generator = MazeGenerator(
        config_dict={
            "HEIGHT": 40,
            "WIDTH": 40,
            "ENTRY": (0, 0),
            "EXIT": (39, 39),
            "PERFECT": True,
            "OUTPUT_FILE": "maze.txt",
        }
    )
    maze = generator.get_maze()
    print(maze)
    print(maze.solution)
    print(maze.seed)
    print("\n\n")

    # Advanced example: instantiate and use with a custom Config object,
    # Then modify the object and get an updated maze
    from mazegen import Config

    config = Config.model_validate({
            "HEIGHT": 40,
            "WIDTH": 40,
            "ENTRY": (0, 0),
            "EXIT": (39, 39),
            "PERFECT": True,
            "OUTPUT_FILE": "maze.txt",
        }
    )

    generator = MazeGenerator(config=config)
    maze = generator.get_maze()
    print(maze)
    config.set("nb_col", 80)
    config.set("perfect", False)

    maze = generator.get_maze()
    print(maze)
