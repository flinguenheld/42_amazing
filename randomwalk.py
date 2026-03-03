from typing import List

def print_tab(tab: List[str]) -> None:
    for line in tab:
        print(line)

def walk(start: Tuple[int, int], tab: List[str]):
    


def random_walk_demo():
    o = 'o'
    x = 'x'
    tab = [10 * o for _ in range(10)]
    print_tab(tab)
    tab[0][0] = x

if __name__ == "__main__":
    random_walk_demo()
