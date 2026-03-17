# mazegen - MazeGenerator class

-------------------------------

## Instantiation

The MazeGenerator class constructor can take a Config class object as argument, 
in which it will seek parameters elements needed for the maze generation. 
For more information, see #Config.
 
For default configuration :
`
from mazegen.maze\_generator import MazeGenerator

generator = MazeGenerator()
`
 
With customized Config object:
`
from mazegen.maze\_generator import MazeGenerator
from mazegen.config import Config

config = Config.model\_validate({"HEIGHT": 20,
                                "WIDTH": 40,
                                "SEED": 42,
                                "ALGO": DFS})
generator = MazeGenerator(config)
`

## Usage

To get direct access to the generated maze, it's parameters and it's solution : 
`
from mazegen.maze\_generator import MazeGenerator

generator = MazeGenerator()
maze = generator.get\_maze()
`
This returns a Maze object, which holds all the relevant informations about itself.
It also includes a break\_wall() method, which takes two tuples of coordinates and 
breaks the wall between both represented cells. 
`
from mazegen.maze\_generator import MazeGenerator

generator = MazeGenerator()
maze = generator.get\_maze()
\# safe is a bool that prevents the creation of cells like 0b0000
maze.break\_wall((0, 0), (0, 1), safe=True)
`
 
> Reminder: cells are hexadecimal values from 0x0 to 0xF whose bytes,
>  from least to most significant, represent North, East, South and West walls. 
 

