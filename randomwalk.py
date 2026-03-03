from typing import List
import random
import time

def print_tab(tab: List):
    for line in tab:
        print(line)
    print("\n\n")

def check_coor(row: int, col: int, tab) -> bool:
    if row < 0 or col < 0 or row > 9 or col > 9:
        return False
    elif tab[row][col] == 1:
        return False
    return True

def rect_coor(row: int, col: int, tab) -> List[int, int]:
    if row < 0:
        return row + 1, col
    if col < 0:
        return row, col + 1
    if row > 9:
        return row - 1, col
    if col > 9:
        return row, col - 1
    return first_empty(row, col, tab)

def first_empty(row: int, col: int, tab) -> List[int, int]:
    if tab[row - 1][col] == 0:
        return row - 1, col
    if tab[row + 1][col] == 0:
        return row + 1, col
    if tab[row][col - 1] == 0:
        return row, col - 1
    if tab[row][col + 1] == 0:
        return row, col + 1

def go_up(coor: List[int, int], tab: List[List[int]]) -> List[int, int]:
    row, col = coor
    return coor 

#def walk(coor: List[int, int], goal: List[int, int], tab: List[List[str]]) -> None:


def random_walk_demo():
    tab = [[0 for _ in range(0, 10)] for _ in range(0, 10)]
    tab[9][9] = 7
    print_tab(tab)
    row, col = 0, 0
    coor = [row, col]
    goal = 9, 9
    #walk(coor, goal, tab)
    #0 = up 1 = right 2 = left 3 = down
    while coor != goal:
        choice = random.randint(0, 3)
        match choice:
            case 0:
                coor = go_up(coor, tab)
            case 1:
                coor = go_right(coor, tab)
            case 2:
                coor = go_left(coor, tab)
            case 3:
                coor = go_down(coor, tab)

    


if __name__ == "__main__":
    random_walk_demo()
