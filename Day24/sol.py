import sys; sys.dont_write_bytecode = True; from utils import *
import math
import sortedcollections
from collections import deque, namedtuple


movements = [[0, 1],[0, -1],[1, 0],[-1, 0]]

inside = [[2,1],[1,2],[2,3],[3,2]]

def getNeighbours(game, pos):
    count = 0
    for m in movements:
        looking = [pos[0] + m[0], pos[1] + m[1]]
        if looking[0] < 0 or looking[0] >= len(game[0]):
            continue
        if looking[1] < 0 or looking[1] >= len(game):
            continue
        else:
            if game[looking[1]][looking[0]] == "#":
                count += 1
    return count

def getNeighbours2(layers, pos, depth):
    count = 0
    if pos in inside and depth + 1 < len(layers):
        if pos == [2, 1]:
            count += layers[depth+1][0].count("#")
        elif pos == [1,2]:
            count += [row[0] for row in layers[depth+1]].count("#")
        elif pos == [2,3]:
            count += layers[depth+1][len(layers[depth+1])-1].count("#")
        elif pos == [3,2]:
            count += [row[len(row) - 1] for row in layers[depth+1]].count("#")
    

    if depth - 1 >= 0:
        if pos[0] == 0:
            if layers[depth-1][2][1] == "#":
                count += 1
        if pos[0] == len(layers[depth][0]) - 1:
            if layers[depth-1][2][3] == "#":
                count += 1
        if pos[1] == 0:
            if layers[depth-1][1][2] == "#":
                count += 1
        if pos[1] == len(layers[depth]) - 1:
            if layers[depth-1][3][2] == "#":
                count += 1
            
    for m in movements:
        looking = [pos[0] + m[0], pos[1] + m[1]]
        if looking == [2,2]:
            continue
        if looking[0] < 0 or looking[0] >= len(layers[depth][0]):
            continue
        if looking[1] < 0 or looking[1] >= len(layers[depth]):
            continue
        else:
            if layers[depth][looking[1]][looking[0]] == "#":
                count += 1

    return count

def bioDiversity(game):
    pos = 0
    score = 0
    for row in game:
        for item in row:
            if item == "#":
                score += (2 ** pos)
            pos += 1
    return score




def do_case(inp: str, sample=False):
    lines = inp.splitlines()
    
    map = defaultdict()
    N = 5
    bugs = 0
    for i in range(0, N):
        for j in range(0, N):
            map[(0,i,j)] = 1 if lines[i][j] == '#' else 0
            if lines[i][j] == '#':
                bugs+=1
    neighbors=defaultdict(set)
    
    portals = [(1,2), (3,2), (2,1), (2,3)]
    for y in range(0, N):
        for x in range(0, N):
            if x > 0 and x < N-1 and y > 0 and y < N-1 and (x,y) not in portals:
                neighbors[(x,y)] = {(0, x-1,y), (0, x+1, y), (0, x, y-1), (0, x, y+1)}
            else:
                if (x,y) not in portals:
                    if x == 0:
                        neighbors[(x,y)] = {(-1, 1, 2), (0, x+1, y)} #, (0, x, y-1), (0, x, y+1)]
                    elif x == N-1:
                        neighbors[(x,y)] = {(0, x-1,y), (-1, 3, 2)} #, (0, x, y-1), (0, x, y+1)]
                    else:
                        neighbors[(x,y)] = {(0, x-1,y),(0, x+1,y)}
                    
                    if y == 0:
                        neighbors[(x,y)] |= {(-1, 2, 1), (0, x, y+1)}
                    elif y == N-1:
                        neighbors[(x,y)] |= {(0, x, y-1), (-1, 2, 3)}
                    else:
                        neighbors[(x,y)] |= {(0, x, y-1), (0, x, y+1)}
                else:
                    if (x,y) == (1,2):
                        neighbors[(x,y)] = {(0, x-1,y), (1, 0, 0),(1, 0, 1),(1, 0, 2),(1, 0, 3),(1, 0, 4),(0, x, y-1), (0, x, y+1)}
                    elif (x,y) == (3,2):
                        neighbors[(x,y)] = {(0, x+1,y), (1, 4, 0),(1, 4, 1),(1, 4, 2),(1, 4, 3),(1, 4, 4),(0, x, y-1), (0, x, y+1)}
                    elif (x,y) == (2,1):
                        neighbors[(x,y)] = {(0, x-1,y),(0, x+1,y),(1, 0, 0),(1, 1, 0),(1, 2, 0),(1, 3, 0),(1, 4, 0),(0, x, y-1)}
                    elif (x,y) == (2,3):
                        neighbors[(x,y)] = {(0, x-1,y),(0, x+1,y),(1, 0, 4),(1, 1, 4),(1, 2, 4),(1, 3, 4),(1, 4, 4),(0, x, y+1)}
                
    def GetNeighbors(l, x, y):
        count = 0
        for (dl, nx, ny) in neighbors[(x,y)]:
            coord = (l+dl, nx, ny)
            count += map[coord] if coord in map.keys() else 0
        return count

    
    data = [list(line) for line in lines]
    game = data[:]

    seenTwice = False
    seen = []
    while not seenTwice:
        if game in seen:
            print("part 1:", bioDiversity(game))
            seenTwice = True
        seen.append(game)
        newGame = [["." for x in range(len(data[0]))] for y in range(len(data))]
        for y, row in enumerate(game):
            for x, item in enumerate(row):
                c = getNeighbours(game, [x, y])
                if item == "#" and c == 1:
                    newGame[y][x] = "#"
                if (item == "." and c == 1) or (item == "." and c == 2):
                    newGame[y][x] = "#"
        game = newGame[:]

    game = data[:]
    minutes = 200
    layers = [[["." for x in range(len(data[0]))] for y in range(len(data))] for i in range((minutes * 2) + 1)]

    layers[minutes] = game
    for layer in layers:
        layer[2][2] = "?"

    count = 16
    affected = [minutes-1,minutes,minutes+1]
    reach = 2
    for i in range(minutes):
        newLayers = layers[:]
        newmap = defaultdict()
        for depth in affected:
            layer = layers[depth]
            newLayer = [["." for x in range(len(data[0]))] for y in range(len(data))]
            newLayer[2][2] = "?"
            for y, row in enumerate(layer):
                for x, item in enumerate(row):
                    c = getNeighbours2(layers, [x, y], depth)
                    sur = GetNeighbors(depth-minutes,y,x)
                    if c != sur:
                        print(c, sur)
                    if item == "?":
                        continue
                    if item == "#":
                        if c == 1:
                            newLayer[y][x] = "#"
                            newmap[(depth-minutes, y, x)] = 1
                        else:
                            newLayer[y][x] = "."
                            newmap[(depth-minutes, y, x)] = 0
                            count-=1
                    if (item == "." and c == 1) or (item == "." and c == 2):
                        newLayer[y][x] = "#"
                        newmap[(depth-minutes, y, x)] = 1
                        count+=1
            newLayers[depth] = newLayer[:]
        layers = newLayers[:]
        map = newmap
        affected += [minutes-reach, minutes+reach]
        reach += 1
    print("part 2 count:", count)

    
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
r"""
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
