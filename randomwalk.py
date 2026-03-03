from typing import List
import numpy
import random
import time

MAX = 9

def print_tab(path: List):
    tab = [[0 for _ in range(0, 10)] for _ in range(0, 10)]
    for row, col in path:
        tab[row][col] = 1
    for line in tab:
        print(line)
    print("\n")


def go_back(path: List[Tuple[int, int]], new_r: int, new_c: int):
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    index = len(path) - 1
    for r, c in moves:
        if (new_r + r, new_c + c) in path:
            new_index = [k for k, v in enumerate(path)
                         if v == (new_r + r, new_c + c)][0]
            if new_index < index:
                index = new_index
    path = path[:index]
    return path

def random_walk_demo():        
    cur_r, cur_c = 0, 0
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    path = [(0, 0)]

    while (cur_r, cur_c) != (MAX, MAX):
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
            print_tab(path)
            cur_r, cur_c = (0, 0) if len(path) == 0 else path[-1]
            time.sleep(0.1)
        else:
            new_r, new_c = valid_moves[random.randint(0, len(valid_moves) - 1)]
            cur_r += new_r
            cur_c += new_c
            path.append((cur_r, cur_c))
            print_tab(path)
            time.sleep(0.1)

if __name__ == "__main__":
    random_walk_demo()
