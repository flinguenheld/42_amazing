*This project has been created as part of the 42 curriculum by flinguen and rapoggi*

# A-Maze-ing

## Descritption

This repository is our version of the A-Maze-ing project from 42's curriculum. 
It written in Python and aims for a better understanding of Python and OOP 
by the generation and display of a perfect (or not) maze. A perfect maze is one 
in which any point A and B are connected by a unique path.

This implies choosing between several algorithms and display libraries, choices 
which will be discussed later on. 

<div align="center">
    <img src="./images/amazing_diagram_01.excalidraw.png">
</div>

## Instructions

This project uses uv for automatic virtual environment management. 

A Makefile has been provided as required. Run: 

    make install
to install dependencies needed by the project. To execute run:

    make run
this will fetch the config.txt file in the repository and pass it to the script 

    make clean
removes cached folders and files, as well as venv and info created by uv 

    make lint
runs flake8 and mypy on current directory

    make lint-strict
runs flake8 and mypy --strict on current directory

Command to fix the pytest import failure:
`uv pip install -e .`

#### Visualiser controls

    TODO List visualiser controls


#### mazegen module instructions

    TODO copy/link mazegen README.md

## Resources

<https://en.wikipedia.org/wiki/Maze_generation_algorithm>
For reference about the Wilson and DFS algorithm for maze generation
<https://geeks4geeks.org>
To answer various Python questions
<https://textual.textualize.io/guide>
For reference about textual - graphical library

## Config File

The config.txt file needs simple but strict encoding of values: KEY=value 
All keys and example values in an example config.txt:

    WIDTH=20
    HEIGHT=20
    ENTRY=0,0
    EXIT=20,20
    PERFECT=False
    LOOP_RATIO=75
    ALGO=Wilson
    SEED=42

Note a default config.txt is already present in the repository. 
Configuration can also be modified either in memory or in file 
through the visualiser. See #Bonus.

## Algorithm

We have implemented both the Wilson and DFS algorithms for maze generation.
 
The Wilson algorithm starts by picking a random start cell and a random end cell. 
It walks, with each step being random, from start to end, and on finish marks 
traversed cells as in-maze.
Then it chooses randomly a not-in-maze cell, and walks again until it reaches an in-maze cell.
And it repeats the last step until no cell is left out of maze.


