import sys; sys.dont_write_bytecode = True; from utils import *
import math
from collections import deque, namedtuple

def do_case(inp: str, sample=False):
    lines = inp.splitlines()
    map = defaultdict()
    portal_coord = defaultdict(list)
    coord_portal = defaultdict()
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            c = lines[y][x]
            map[(x,y)] = c
            if c >= 'A' and c<='Z':
                if y == 0:
                    portal_id = c + lines[y+1][x]
                    portal_coord[portal_id].append((x,y+2))
                    coord_portal[((x,y+2),-1)] = portal_id
                elif y == len(lines) - 1:
                    portal_id = lines[y-1][x] + c
                    portal_coord[portal_id].append((x,y-2))
                    coord_portal[((x,y-2),-1)] = portal_id
                elif x == 0:
                    portal_id = c + lines[y][x+1]
                    portal_coord[portal_id].append((x+2,y))
                    coord_portal[((x+2,y),-1)] = portal_id
                elif x == len(lines[0]) - 1:
                    portal_id = lines[y][x-1] + c
                    portal_coord[portal_id].append((x-2,y))
                    coord_portal[((x-2,y),-1)] = portal_id
                elif x > 2 and x < len(lines[0])-2 and lines[y][x-1] == '.':
                    portal_id = c+lines[y][x+1] 
                    portal_coord[portal_id].append((x-1,y))
                    coord_portal[((x-1,y),1)] = portal_id
                elif x > 2 and x < len(lines[0])-2 and lines[y][x+1] == '.':
                    portal_id = lines[y][x-1] + c
                    portal_coord[portal_id].append((x+1,y))
                    coord_portal[((x+1,y),1)] = portal_id
                elif y > 2 and y < len(lines)-2 and lines[y-1][x] == '.':
                    portal_id = c + lines[y+1][x]
                    portal_coord[portal_id].append((x,y-1))
                    coord_portal[((x,y-1),1)] = portal_id
                elif y > 2 and y < len(lines)-2 and lines[y+1][x] == '.':
                    portal_id = lines[y-1][x] + c
                    portal_coord[portal_id].append((x,y+1))
                    coord_portal[((x,y+1),1)] = portal_id
    
    #print(portal_coord)
    #print(coord_portal)
    start = portal_coord['AA'][0]
    end = portal_coord['ZZ'][0]
    portal_coord.pop('AA')
    portal_coord.pop('ZZ')
    coord_portal.pop((start,-1))
    coord_portal.pop((end, -1))
    print(start, end)
    
    q = deque()
    q.append((start, 0, 0))
    
    visited = set()
    visited.add((start,0))
    while(len(q) > 0):
        cur = q.popleft()
        c = cur[0]
        level = cur[2]
        visited.add((c,level))
        if (c,level) == (end,0):
            print(cur[1])
            return
        if level < len(portal_coord) and (c,1) in coord_portal:
            for coord in portal_coord[coord_portal[(c,1)]]:
                if coord != c and not (coord, level+1) in visited:
                    q.append((coord,cur[1]+1, level+1))
        elif level > 0 and (c,-1) in coord_portal:
            for coord in portal_coord[coord_portal[(c,-1)]]:
                if coord != c and not (coord, level-1) in visited:
                    q.append((coord,cur[1]+1, level-1))
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
            x = c[0]+dx
            y = c[1]+dy
            if map[(x,y)] == '.' and not ((x,y), level) in visited:
                q.append(((x,y),cur[1]+1, level))
            
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
