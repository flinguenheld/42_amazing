# mazegen - MazeGenerator class

-------------------------------

## Instantiation

The MazeGenerator class constructor can take a Config class object as argument, 
in which it will seek parameters elements needed for the maze generation. 
For more information, see #Config.
 
For default configuration :

    from mazegen.maze_generator import MazeGenerator
    
    generator = MazeGenerator()

 
With customized Config object:

    from mazegen.maze_generator import MazeGenerator
    from mazegen.config import Config

    config = Config.model_validate({"HEIGHT": 20,
                                    "WIDTH": 40,
                                    "SEED": 42,
                                    "ALGO": "Wilson"})
    generator = MazeGenerator(config)


## Usage

To get direct access to the generated maze, it's parameters and it's solution : 

    from mazegen.maze_generator import MazeGenerator
    
    generator = MazeGenerator()
    maze = generator.get_maze()

This returns a Maze object, which holds all the relevant informations about itself.
It also includes a break\_wall() method, which takes two tuples of coordinates and 
breaks the wall between the two represented cells. 

    from mazegen.maze_generator import MazeGenerator
    
    generator = MazeGenerator()
    maze = generator.get_maze()
    print(maze.solution)
    # safe is a bool that prevents the creation of cells like 0b0000
    maze.break_wall((0, 0), (0, 1), safe=True)

 
> Reminder: cells are hexadecimal values from 0x0 to 0xF whose bytes,
>  from least to most significant, represent North, East, South and West walls. 

get\_maze() skips to the very last element yielded by a generator (generate()) 
and returns it. If you wish to animate the generation or only use generated data 
up to a certain point, you may also use generate():

    from mazegen.maze_generator import MazeGenerator

    generator = MazeGenerator()
    for maze in generator.generate():
        print(maze)

The actual maze (two-dimensional array of hexadecimal values) 
    is stored in maze.values

Maze's \_\_str\_\_() returns the maze in hexadecimal values, entry and exit 
coordinates, and instructions to 'walk' from one to the other. 

## Config

To customize the generated maze, we would use a Config object passed to MazeGenerator
on initialization. The Config class inherits from pydantic's BaseModel and runs various
data sanity related checks to ensure coherent data is going to end up in the maze.

Config().model\_validate() can be given a dictionnary whose keys define which 
parameter is set and it's values... the value.
It can also be modified after initialisation through it's setter, here an example of both:

    from mazegen.maze_generator import MazeGenerator

    # Initialises config with default values
    temp_config = Config()
    del temp_config

    # Initalises config with custom dict (by alias)
    config = Config.model_validate({"WIDTH": 40,
                                    "HEIGHT": 20,
                                    "SEED": 42,
                                    "ALGO": DFS})

    # Sets new values after initialisation (by attr name)
    config.set("perfect", False)
    config.set("loop_ratio", 75)

    generator = MazeGenerator(config)
    maze = generator.get_maze()

Data always gets routed through checks before assignation. 
Here are all parameters and their default value:

| Parameter | Alias   | Default |
| --------- | ------- | ------- |
| nb\_col   | WIDTH   | 15      |
| nb\_row   | HEIGHT  | 15      |
| entry     | ENTRY   | (0, 0)  |
| exit      | EXIT    | (14, 14)|
| output\_file | OUTPUT\_FILE | maze.txt |
| perfect   | PERFECT | False   |
| seed      | SEED    | date+"AUTO"+time |
| algo      | ALGO    | Wilson  |
| loop\_ratio | LOOP\_RATIO | 100 |

The Config class also provides a getter (get()) which defaults to None 
if there are no attributes of the given name. 

## Additional

Calling MazeGenerator's generate(), then modifying the config, 
then calling generate() again will result in a new, updated maze of 
parameters specified in newly modified Config. 

The seed's default value isn't set in the Config itself but MazeGenerator, 
to allow for a different seed each run if none was set on instantiation. 
