import sys; sys.dont_write_bytecode = True; from utils import *
import queue
import math


def do_case(inp: str, sample=False):
    lines = inp.splitlines()
    formulas = defaultdict(list)
    store = defaultdict()
    for l in lines:
        parts = l.split(' => ')
        ins = parts[0].split(', ')
        outs = parts[1].split(' ')
        outs_n = int(outs[0])
        outs_e = outs[1]
        store[outs_e] = 0
        reqs = [(outs_e, outs_n)]
        for i in ins:
            part = i.split(' ')
            n = int(part[0])
            e = part[1]
            reqs.append((e,n))
            store[e] = 0
        formulas[outs_e]=reqs
    def collect(e, amt):
        if e == 'ORE':
            return amt
        else:
            n = 0
            produced = formulas[e][0][1]
            amt -= store[e]
            k = math.ceil(amt / produced)
            store[e] = k * produced - amt
            for i in range(1, len(formulas[e])):
                n += collect(formulas[e][i][0], k*formulas[e][i][1])
        return n
    #print(collect('FUEL', 1))
    
    #part 2
    a, b = 1, 2
    while collect('FUEL',b) < 10**12:
        a, b = b, b * 2
        for e in store:
            store[e] = 0
    while b - a >= 2:
        half = a + (b - a) // 2
        if collect('FUEL',half) > 10**12:
            b = half
        else:
            a = half
        for e in store:
            store[e] = 0
    print(a)
    
    
        
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
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
