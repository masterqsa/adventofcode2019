import sys; sys.dont_write_bytecode = True; from utils import *
import queue

class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.hidden = set()

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    map = defaultdict()
    map_list = list()
    map_counts = defaultdict()
    lines = inp.splitlines()
    m = len(lines)
    n = len(lines[0])
    for i in range(0, n):
        map[i] = defaultdict(bool)
        map_counts[i] = defaultdict(int)
    for j in range(0, m):
        for i in range(0, n):
            if lines[j][i] == '#':
                map[i][j] = True    
                map_list.append(Point(i, j))
                
    def simplify(dx, dy):
        if dx == 0:
            return 0, 1
        elif dy == 0:
            return 1, 0
        m = min(abs(dx), abs(dy))
        i = 2
        while i <= m:
            if dx % i == 0 and dy % i == 0:
                dx = dx // i
                dy = dy // i
            else:
                i += 1
        return dx, dy
    
    #print(simplify(-4,6)) # -> -2, 3
    
    def hide(first, second):
        dx = second.x - first.x
        dy = second.y - first.y
        dx, dy = simplify(dx, dy)
        x = second.x + dx
        y = second.y + dy
        while x >= 0 and x < n and y >= 0 and y < m:
            if map[x][y]: #found asteroid at hidden position
                first.hidden.add((x,y))
            x += dx
            y += dy
    max_count = 0
    best_x = -1
    best_y = -1
    for i in range(0, len(map_list) - 1):
        first = map_list[i]
        for j in range(i + 1, len(map_list)):
            second = map_list[j]
            if not (second.x, second.y) in first.hidden:
                map_counts[first.x][first.y]+=1
                if max_count < map_counts[first.x][first.y]:
                    max_count = map_counts[first.x][first.y]
                    best_x = first.x
                    best_y = first.y
                map_counts[second.x][second.y]+=1
                if max_count < map_counts[second.x][second.y]:
                    max_count = map_counts[second.x][second.y]
                    best_x = second.x
                    best_y = second.y
                hide(first, second)
    
    print(max_count, best_x, best_y)
    
    # Part 2
    center_x = best_x
    center_y = best_y
    q1 = set()
    q1.add((0, 1))
    for i in range(center_x + 1, n):
        for j in range(0, center_y):
            if map[i][j]:
                q1.add(simplify(i - center_x, j - center_y))
    q1_list = list(q1)
    q1_list.sort(key = lambda a: - a[0] / a[1])
    q2 = set()
    q2.add((1, 0))
    for i in range(center_x + 1, n):
        for j in range(center_y, m):
            if map[i][j]:
                q2.add(simplify(i - center_x, j - center_y))
    q2_list = list(q2)
    q2_list.sort(key = lambda a: a[1] / a[0])
    q3 = set()
    q3.add((0, -1))
    for i in range(0, center_x):
        for j in range(center_y + 1, m):
            if map[i][j]:
                q3.add(simplify(i - center_x, j - center_y))
    q3_list = list(q3)
    q3_list.sort(key = lambda a: - a[0] / a[1])
    q4 = set()
    q4.add((-1, 0))
    for i in range(0, center_x):
        for j in range(0, center_y):
            if map[i][j]:
                q4.add(simplify(i - center_x, j - center_y))
    q4_list = list(q4)
    q4_list.sort(key = lambda a: a[1] / a[0])
    combined = q1_list + q2_list + q3_list + q4_list
    i = 0
    
    while i < 200:
        for dx, dy in combined:
            x = center_x + dx
            y = center_y + dy
            while x >= 0 and x < n and y >= 0 and y < m:
                if map[x][y]: #found asteroid at hidden position
                    map[x][y] = False
                    i += 1
                    if i == 200:
                        print(x*100 + y)
                    break
                
                x += dx
                y += dy
                
                
            if i == 200:
                    break
    print(x, y)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""
""",r"""
""",r"""
""",r"""
""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
