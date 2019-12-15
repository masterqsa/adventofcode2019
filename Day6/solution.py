import sys; sys.dont_write_bytecode = True; from utils import *
from dataclasses import dataclass, field
from typing import Any


def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    orbits = defaultdict(list)
    centers = defaultdict()
    for l in lines:
        planets = l.split(')')
        orbits[planets[0]].append(planets[1])
        centers[planets[1]] = planets[0]
        
    visited = set()
    q = []
    for p in orbits:
        if p not in centers:
            com = p
    #print(com)
    q.append(com)
    length = 0
    sum = 0
    while len(q) > 0:
        count = len(q)
        length += 1
        for i in range(0, count):
            p = q.pop(0)
            for sat in orbits[p]:
                if sat not in visited:
                    visited.add(sat)
                    sum += length
                    q.append(sat)
                
    print(sum)
    
    cur = 'YOU'
    length = 0
    track = defaultdict()
    while cur != 'COM':
        length += 1
        cur = centers[cur]
        track[cur] = length
    
    cur = 'SAN'
    length = 0
    while cur != 'COM':
        length += 1
        cur = centers[cur]
        if cur in track:
            print(length + track[cur] - 2)
            return
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
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
