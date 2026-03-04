from typing import List
import sys
import numpy
import random
import time

MAX = 27

BEGIN: Tuple[int, int] = (0, 0)
GOAL: Tuple[int, int] = (26, 26)

def make_tab(path: List[Tuple[int, int]]) -> List[List[int]]:
    tab = [[0 for _ in range(0, MAX + 1)] for _ in range(0, MAX + 1)]
    for row, col in path:
        tab[row][col] = 1
    return tab


def print_tab(path: List):
    tab = make_tab(path)
    for line in tab:
        print(line)
    print("\n")

def flood_fill(tab: List[List[int]], path: List[Tuple[int, int]],
               coor: Tuple[int, int]) -> Tuple[int, int]: 
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    cur_r, cur_c = coor
    valid_moves = []
    new_r, new_c = 0, 0
    for (dir_r, dir_c) in moves:
        new_r = cur_r + dir_r
        new_c = cur_c + dir_c
        if new_r >= 0 and new_r <= MAX and new_c >= 0 and new_c <= MAX:
            target = (new_r, new_c)
            if target not in path:
                valid_moves.append((dir_r, dir_c))

    if len(valid_moves) > 0:
        return coor
    else:
        valid_moves = []
        new_r, new_c = 0, 0
        for (dir_r, dir_c) in moves:
            new_r = cur_r + dir_r
            new_c = cur_c + dir_c
            if new_r >= 0 and new_r <= MAX and new_c >= 0 and new_c <= MAX:
                valid_moves.append((dir_r, dir_c))    
        op = random.choice(valid_moves)
        cur_r += op[0]
        cur_c += op[1]
        return flood_fill(tab, path, (cur_r, cur_c))

def find_first_possible_move(path: List[Tuple[int, int]], 
                             begin: Tuple[int, int]) -> Tuple[int, int]:
    tab = make_tab(path)

    return flood_fill(tab, path, begin)


def go_back(path: List[Tuple[int, int]], new_r: int, new_c: int):
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    index = len(path) - 1
    if 1 <= new_r <= MAX - 1 and 1 <= new_c <= MAX - 1:
        for r, c in moves:
            if (new_r + r, new_c + c) in path:
                new_index = [k for k, v in enumerate(path)
                             if v == (new_r + r, new_c + c)][0]
                if new_index < index:
                    index = new_index
    else:
        r, c = find_first_possible_move(path, path[-1])
        index = [k for k, v in enumerate(path) if v == (r, c)][0]
    path = path[:index]
    return path

def random_walk_demo():        
    cur_r, cur_c = BEGIN
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    path = [(0, 0)]

    while (cur_r, cur_c) != GOAL:
        valid_moves = []
        new_r, new_c = 0, 0
        for (dir_r, dir_c) in moves:
            new_r = cur_r + dir_r
            new_c = cur_c + dir_c
            if new_r >= 0 and new_r <= MAX and new_c >= 0 and new_c <= MAX:
                target = (new_r, new_c)
                if target not in path:
                    valid_moves.append((dir_r, dir_c))

        if len(valid_moves) == 0:
            path = go_back(path, new_r, new_c)
            cur_r, cur_c = (0, 0) if len(path) == 0 else path[-1]
        #    time.sleep(0.01)
        else:
            new_r, new_c = valid_moves[random.randint(0, len(valid_moves) - 1)]
            cur_r += new_r
            cur_c += new_c
            path.append((cur_r, cur_c))
        #    time.sleep(0.01)
    print_tab(path)

if __name__ == "__main__":
    random_walk_demo()
