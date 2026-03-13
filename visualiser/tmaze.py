from maze_generator.maze_generator import MazeGenerator
from io import StringIO
from textual.widgets import Static
from textual.app import RenderResult
from maze_generator.maze import Maze
from textual.reactive import reactive
from visualiser.borders import Borders
from visualiser.mcell import MCellHorizontal, MCellVertical, MCellAngle

# General explanations :
#
# The maze is a List[List[int]]
# Each maze's cell contains an int which represents the walls around itself.
#
# The first four bits are used as well:
#
#   LEFT   BOTTOM   RIGHT   TOP
#    0       1       1       0
#
# This cell with the value 0x6 looks like that:
#
#             ┏━━━
#             ┃
#
# --
# Since we are in a terminal, we have to draw each cell with
# a (or several) characters.
# To do so, we have to surround each cell with walls
# Here for one maze's cell:
# ┏━━━━┳━━━━━━━━┳━━━━┓
# ┃ TL ┃  TOP   ┃ TR ┃
# ┣━━━━╋━━━━━━━━╋━━━━┫
# ┃ L  ┃  Cell  ┃ R  ┃
# ┣━━━━╋━━━━━━━━╋━━━━┫
# ┃ BL ┃  BOT   ┃ BR ┃
# ┗━━━━┻━━━━━━━━┻━━━━┛
#
# Wall mixed up together
# Here for three:
# ┏━━━━┳━━━━━━━━┳━━━━┳━━━━━━━━┳━━━━┳━━━━━━━━┳━━━━┓
# ┃    ┃        ┃    ┃        ┃    ┃        ┃    ┃
# ┣━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━┫
# ┃    ┃  HEXA  ┃    ┃  HEXA  ┃    ┃  HEXA  ┃    ┃
# ┣━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━╋━━━━━━━━╋━━━━┫
# ┃    ┃        ┃    ┃        ┃    ┃        ┃    ┃
# ┗━━━━┻━━━━━━━━┻━━━━┻━━━━━━━━┻━━━━┻━━━━━━━━┻━━━━┛
#
# So TMaze will have three objects:
#   - angles
#   - verticals
#   - horizontals
#
# They will contains wall coordinates and they will be able to return the
# str representation of them at a given coordinate
#
# Then these objects will be used to build the str representation of the full
# maze and refresh the widget automaticaly


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░▀▀█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░▄▀░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀
class TMaze(Static):
    __to_print = reactive("My ass")

    # TODO: CONFIG ! FIND A GOOD WAY TO DEAL WITH ############################
    def __init__(self, config, borders: Borders) -> None:
        super().__init__()
        self.__borders = borders
        # REMOVE TO USE A ONE SHOT IN NEW_MAZE ???????
        # self.__generator = MazeGenerator(config)
        self.__config = config

        # self.new_maze()
        # self.__maze_generator = MazeGenerator(self.__config)
        self.new_animation()

    # ########################################################## NEW MAZE ####
    def new_animation(self):
        # TODO: move that in the constuctor ! ################################
        self.__maze_generator = MazeGenerator(self.__config)
        self.__generator = self.__maze_generator.generate(animate=True)
        self.next_step_animation()

    def next_step_animation(self) -> bool:
        maze = next(self.__generator, None)
        if maze:
            self.__hexa_maze = maze
            self.new_maze()
            return True
        else:
            return False

    def new_maze(self) -> None:
        # generator = MazeGenerator(self.__config)
        # self.__hexa_maze = generator.generate()

        self.__nb_row = self.__hexa_maze.nb_row * 2 + 1
        self.__nb_col = self.__hexa_maze.nb_col * 2 + 1

        self.__angles = MCellAngle(self.__borders)
        self.__verticals = MCellVertical(self.__borders)
        self.__horizontals = MCellHorizontal(self.__borders)

        self.__load_maze()
        self.refresh_maze()

    # ######################################################### LOAD MAZE ####
    def __load_maze(self) -> None:
        """Convert the hexadecimal maze into the TMaze logic

        ┏━━━━┳━━━━━━━━┳━━━━┓
        ┃ TL ┃  TOP   ┃ TR ┃
        ┣━━━━╋━━━━━━━━╋━━━━┫
        ┃ L  ┃  Cell  ┃ R  ┃
        ┣━━━━╋━━━━━━━━╋━━━━┫
        ┃ BL ┃  BOT   ┃ BR ┃
        ┗━━━━┻━━━━━━━━┻━━━━┛
        """

        for rh, row_hexa in enumerate(self.__hexa_maze.values):
            for ch, cell_hexa in enumerate(row_hexa):
                # Who is active ?
                top = cell_hexa & 0b0001 == 0b0001
                left = cell_hexa & 0b1000 == 0b1000
                right = cell_hexa & 0b0010 == 0b0010
                bottom = cell_hexa & 0b0100 == 0b0100

                # Get the top left coordinate in self.cells
                row = rh * 2
                col = ch * 2

                #                                                  -- Top Left
                self.__angles.up(row=row, col=col, bottom=left, right=top)

                #                                                       -- Top
                self.__horizontals.add(row, col + 1, is_active=top)

                #                                                 -- Top Right
                self.__angles.up(row, col + 2, left=top, bottom=right)

                #                                                     -- Right
                self.__verticals.add(row + 1, col + 2, is_active=right)

                #                                              -- Bottom Right
                self.__angles.up(row + 2, col + 2, left=bottom, top=right)

                #                                                    -- Bottom
                self.__horizontals.add(row + 2, col + 1, is_active=bottom)

                #                                               -- Bottom Left
                self.__angles.up(row + 2, col, right=bottom, top=left)

                #                                                      -- Left
                self.__verticals.add(row + 1, col, is_active=left)

    # ########################################################### REFRESH ####
    def refresh_maze(self) -> None:
        """Update the maze str representation"""

        buffer = StringIO("")
        for row in range(0, self.__nb_row):
            buffer.write("\n")
            for col in range(0, self.__nb_col):
                match (row % 2 == 0, col % 2 == 0):
                    case (True, True):
                        buffer.write(self.__angles.to_str(row, col))
                    case (True, False):
                        buffer.write(self.__horizontals.to_str(row, col))
                    case (False, True):
                        buffer.write(self.__verticals.to_str(row, col))
                    case (False, False):
                        if self.__hexa_maze.values[row // 2][col // 2] >= 0xF:
                            buffer.write("░░░")
                        else:
                            buffer.write("   ")

        self.__to_print = buffer.getvalue()

    # ############################################################ RENDER ####
    def render(self) -> RenderResult:
        return self.__to_print
