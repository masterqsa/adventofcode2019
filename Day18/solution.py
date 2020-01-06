import sys; sys.dont_write_bytecode = True; from utils import *
import math
from collections import deque, namedtuple

def do_case(inp: str, sample=False):
    lines = inp.splitlines()
    # map = defaultdict()
    # keys = defaultdict()
    # doors = defaultdict()
    # collected_keys = set()
    # m = len(lines)
    # n = len(lines[0])
    
    # for y in range(0, m):
    #     for x in range(0, n):
    #         map[(x,y)] = lines[y][x]
    #         if lines[y][x] >= 'a' and lines[y][x] <= 'z':
    #             keys[lines[y][x]]=(x,y)
    #         elif lines[y][x] >= 'A' and lines[y][x] <= 'Z':
    #             doors[lines[y][x]]=(x,y)
    #         elif lines[y][x] == '@':
    #             entrance = (x,y)
    #             map[(x,y)] = '.'
    
    # def FindPath(a, b, avail_keys):
    #     visited = set()
    #     q = queue.Queue()
    #     q.put((a, 0))
    #     while q.qsize() > 0:
    #         c = q.get()
    #         for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    #             x = c[0][0]+dx
    #             y = c[0][1]+dy
    #             cell = map[(x,y)]
    #             if (x, y) in visited:
    #                 continue
    #             if (x >=0 and x < n and y >=0 and y < m) and (cell == '.' or cell in keys.keys() or cell.lower() in avail_keys):
    #                 if (x, y) == b:
    #                     return c[1]+1
    #                 else:
    #                     q.put(((x, y), c[1]+1))
    #                     visited.add((x, y))
    #     return -1
    # def BFS(start, avail_keys):
    #     new_keys = list()
    #     visited = set()
    #     q = queue.Queue()
    #     q.put((start, 0))
    #     while q.qsize() > 0:
    #         c = q.get()
    #         for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    #             x = c[0][0]+dx
    #             y = c[0][1]+dy
    #             cell = map[(x,y)]
    #             if (x, y) in visited:
    #                 continue
    #             if (x >=0 and x < n and y >=0 and y < m) and (cell == '.' or cell in keys.keys() or cell.lower() in avail_keys):
    #                 if cell in keys.keys() and not cell in avail_keys:
    #                     new_keys.append(cell)
    #                 else:
    #                     q.put(((x, y), c[1]+1))
    #                     visited.add((x, y))
    #     return new_keys
    
    # ret = 1
    # ordered_keys = list()
    # key_groups = defaultdict()
    # base_keys = set()
    # while(ret > 0):
    #     new_keys = BFS(entrance, collected_keys)
    #     if len(collected_keys) == 0:
    #         key_groups['@'] = new_keys
    #         print('@', new_keys)
    #     ret = len(new_keys)
    #     for k in new_keys:
    #         collected_keys = base_keys
    #         collected_keys.add(k)
    #         local_keys = BFS(entrance, collected_keys)
    #         key_groups[k] = local_keys
    #         print(k, local_keys)
        
    #     for x in new_keys:
    #         collected_keys.add(x)
    #         ordered_keys.append(x)
    #         base_keys.add(x)
    
    # av_keys = set()
    # start = entrance
    # path = 0
    # for k in ordered_keys:
    #     path+=FindPath(start, keys[k], av_keys)
    #     av_keys.add(k)
    #     start = keys[k]
    # print(path)
    
    # sorted_keys = list(keys.keys())
    # sorted_keys.sort()
    # sorted_keys_str = ''.join(sorted_keys)
    # keys['@'] = entrance
    # def TSP(start, current_sum, visited_str):
    #     if visited_str == sorted_keys_str:
    #         return current_sum
    #     visited = set()
    #     for c in visited_str:
    #         visited.add(c)
    #     best = 99999999
    #     for next in key_groups[start]:
    #         start_to_next = FindPath(keys[start], keys[next], visited)
    #         l = list(visited)
    #         l.append(next)
    #         l.sort()
    #         dist = TSP(next, current_sum + start_to_next, ''.join(l))
    #         if dist < best:
    #             best = dist
    #     return best
    # print(TSP('@', 0, ''))
    
    #Part 1
    # G = []
    # for line in lines:
    #     G.append(list(line.strip()))
    # R = len(G)
    # C = len(G[0])
    # DR = [-1,0,1,0]
    # DC = [0,1,0,-1]
    # Q = deque()
    # State = namedtuple('State', ['r', 'c', 'keys', 'd'])
    # all_keys = set()
    # for r in range(R):
    #     for c in range(C):
    #         if G[r][c]=='@':
    #             print(r,c,G[r][c])
    #             Q.append(State(r, c, set(), 0))
    #         if 'a'<=G[r][c]<='z':
    #             all_keys.add(G[r][c])
    # print(len(all_keys), all_keys)

    # SEEN = set()
    # while Q:
    #     S = Q.popleft()
    #     key = (S.r, S.c, tuple(sorted(S.keys)))
    #     #print(key)
    #     if key in SEEN:
    #         continue
    #     SEEN.add(key)
    #     if len(SEEN)%100000 == 0:
    #         print(len(SEEN))
    #     if not (0<=S.r<R and 0<=S.c<C and G[S.r][S.c]!='#'):
    #         continue
    #     if 'A'<=G[S.r][S.c]<='Z' and G[S.r][S.c].lower() not in S.keys:
    #         continue
    #     newkeys = set(S.keys)
    #     if 'a'<=G[S.r][S.c]<='z':
    #         newkeys.add(G[S.r][S.c])
    #         if newkeys == all_keys:
    #             print(S.d)
    #             sys.exit(0)
    #     for d in range(4):
    #         rr,cc = S.r+DR[d], S.c+DC[d]
    #         Q.append(State(rr, cc, newkeys, S.d+1))
    
    G = []
    for line in lines:
        G.append(list(line.strip()))
    R = len(G)
    C = len(G[0])
    DR = [-1,0,1,0]
    DC = [0,1,0,-1]
    Q = deque()
    State = namedtuple('State', ['pos', 'keys', 'd'])
    all_doors = {}
    all_keys = {}
    starts = []
    for r in range(R):
        for c in range(C):
            if G[r][c]=='@':
                starts.append((r,c))
            if 'a'<=G[r][c]<='z':
                all_keys[G[r][c]] = (r,c)
            if 'A'<=G[r][c]<='Z':
                all_doors[G[r][c]] = (r,c)
    print(len(all_keys), all_keys)
    print(len(all_doors), all_doors)
    Q.append(State(starts, set(), 0))
    N = len(starts)

    best = 1e9
    SEEN = {}
    while Q:
        S = Q.popleft()
        key = (tuple(S.pos), tuple(sorted(S.keys)))
        if key in SEEN and S.d>=SEEN[key]:
            continue
        SEEN[key] = S.d
        if len(SEEN)%10000 == 0:
            print(key,S.d)
            print(len(SEEN))
        newkeys = set(S.keys)
        bad = False
        for i in range(N):
            r,c = S.pos[i]
            if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
                bad = True
                break
            if 'A'<=G[r][c]<='Z' and G[r][c].lower() not in S.keys:
                bad = True
                print('B2')
                break
        if bad:
            continue

        D = {}
        Q2 = deque()
        for i in range(N):
            Q2.append((S.pos[i], i, 0))
        while Q2:
            pos,robot,dd = Q2.popleft()
            r,c = pos
            if not (0<=r<R and 0<=c<C and G[r][c]!='#'):
                continue
            if 'A'<=G[r][c]<='Z' and G[r][c].lower() not in S.keys:
                continue
            if pos in D:
                continue
            D[pos] = (dd,robot)
            for d3 in range(4):
                newpos = (r+DR[d3], c+DC[d3])
                Q2.append((newpos, robot,dd+1))

        for k in all_keys:
            if k not in S.keys and all_keys[k] in D:
                distance,robot = D[all_keys[k]]
                newpos = list(S.pos)
                newpos[robot] = all_keys[k]
                newkeys = set(S.keys)
                newkeys.add(k)
                newdist = S.d+distance
                if len(newkeys) == len(all_keys):
                    if newdist < best:
                        best = newdist
                        print(best)
                Q.append(State(newpos, newkeys, newdist))

    
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
