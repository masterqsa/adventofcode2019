import sys; sys.dont_write_bytecode = True; from utils import *
import math
from collections import deque, namedtuple

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
                
            
    def GetSide(l, x, y):
        count = 0
        if y == 2:
            xx = 0 if x==1 else N-1
            for j in range(0,N):
                coord = (l, xx, j)
                count+= map[coord] if coord in map.keys() else 0
        elif x == 2:
            yy = 0 if y==1 else N-1
            for j in range(0,N):
                coord = (l, j, yy)
                count+= map[coord] if coord in map.keys() else 0
        return count
    
    def Surrounding(l, x, y):
        count = 0
        if x > 0:
            coord = (l, x-1, y)
            count += (map[coord] if coord in map.keys() else 0) if (x,y) != (3,2) else GetSide(l+1, x, y)
        else:
            coord = (l-1, 1, 2)
            count += map[coord] if coord in map.keys() else 0
            
        if x < N-1:
            coord = (l, x+1, y)
            count += (map[coord] if coord in map.keys() else 0) if (x,y) != (1,2) else GetSide(l+1, x, y)
        else:
            coord = (l-1, 3, 2)
            count += map[coord] if coord in map.keys() else 0
            
        if y > 0:
            coord = (l, x, y-1)
            count += (map[coord] if coord in map.keys() else 0) if (x,y) != (2,3) else GetSide(l+1, x, y)
        else:
            coord = (l-1, 2, 1)
            count += map[coord] if coord in map.keys() else 0
            
        if y < N-1:
            coord = (l, x, y+1)
            count += (map[coord] if coord in map.keys() else 0) if (x,y) != (2,1) else GetSide(l+1, x, y)
        else:
            coord = (l-1, 2, 3)
            count += map[coord] if coord in map.keys() else 0
        return count
    
    def GetNeighbors(l, x, y):
        count = 0
        for (dl, nx, ny) in neighbors[(x,y)]:
            coord = (l+dl, nx, ny)
            count += map[coord] if coord in map.keys() else 0
        return count
    
    def Biodiversity():
        res = 0
        for i in range(0, N):
            for j in range(0, N):
                if map[(0,i,j)] == 1:
                    res += (1<<(i * N + j))
        return res
    
    # observed = set()  
    # observed.add(Biodiversity())   
    for step in range(0, 200):
        # print(bugs)
        newmap = defaultdict()
        for l in range(-step-1, step+2):
            for i in range(0, N):
                for j in range(0, N):
                    if (i,j) == (2,2):
                        continue
                    sur = GetNeighbors(l,i,j)
                    if sur != 1 and (l,i,j) in map.keys() and map[(l,i,j)] == 1:
                        newmap[(l,i,j)] = 0
                        bugs-=1
                    elif (sur == 1 or sur == 2) and ((l,i,j) not in map.keys() or map[(l,i,j)] == 0):
                        newmap[(l,i,j)] = 1
                        bugs+=1
                    else:
                        newmap[(l,i,j)] = map[(l,i,j)] if (l,i,j) in map.keys() else 0
        map = newmap
        
        # level = 5
        # for i in range(0, N):
        #     s = ""
        #     for j in range(0, N):
        #         if (i,j) == (2,2):
        #             s+='?'
        #         else:
        #             s+='#' if (level, i, j) in map.keys() and map[(level, i, j)] == 1 else '.'
        #     print(s)
        # print("")
        # bd = Biodiversity()
        # if bd in observed:
        #     print(bd)
        #     break
        # else:
        #     observed.add(bd)
        
    # 2306, 2021 too low is not right
    # for i in range(0, N):
    #     s = ""
    #     for j in range(0, N):
    #         if (i,j) == (2,2):
    #             s+='?'
    #         else:
    #             s+='#' if map[(0, i, j)] == 1 else '.'
    #     print(s)
    print(bugs)
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
