import sys; sys.dont_write_bytecode = True; from utils import *
import math
from collections import deque, namedtuple

N = 119315717514047 #10007
CUT = 1
DEALSTACK = 2
DEALINCR = 3

def eucledean_gcd(a, b):
    if b==0:
        return a,1,0  # a == gcd(a,0) == 1*a + 0*0
    d,x,y = eucledean_gcd(b, a%b)
    return d, y, x - (a//b)*y
    
def modinv(a, m):
    g, x, y = eucledean_gcd(a, m)
    if g == 1:
        return x % m
    return 0
        

class Rule:
    def __init__(self, _type, _param : int):
        self.type = _type
        self.param = _param
        
    def GetPriorPosition(self, _pos : int):
        if self.type == CUT:
            return (_pos + N + self.param) % N
        elif self.type == DEALSTACK:
            return N - 1 - _pos
        else:
            return modinv(self.param, N) * _pos%N

def do_case(inp: str, sample=False):
    n = N
    # deck = list()
    # newdeck = list()
    # for i in range(0,n):
    #     deck.append(i)
    lines = inp.splitlines()
    # cut -6593
    # deal into new stack
    # deal with increment 54
    # for l in lines:
    #     split = l.split(' ')
    #     if split[0] == 'cut':
    #         m = int(split[1])
    #         if m < 0:
    #             m = n + m
    #         deck = deck[m:]+deck[:m]
    #     elif split[0] == 'deal':
    #         if split[1] == 'into':
    #             deck.reverse()
    #         else:
    #             m = int(split[3])
    #             newdeck = [None]*n
    #             for i in range(0, n):
    #                 newdeck[(m * i)%N] = deck[i]
    #             deck = newdeck
    #print(deck)           
    # print(deck[2019])
    # for i in range(0, n):
    #     if deck[i] == 2019:
    #         print(i)
    
    #Part 2
    
    rules = []
    for l in lines:
        split = l.split(' ')
        if split[0] == 'cut':
            m = int(split[1])
            if m < 0:
                m = n + m
            rules.append(Rule(CUT, m))
        elif split[0] == 'deal':
            if split[1] == 'into':
                rules.append(Rule(DEALSTACK, 0))
            else:
                m = int(split[3])
                rules.append(Rule(DEALINCR, m))
    
    iterations = 101741582076661
    rules.reverse()
    rulessize = len(rules)
    position = 2020
    x = position
    for r in range(0, rulessize):
        position = rules[r].GetPriorPosition(position)
    y = position
    for r in range(0, rulessize):
        position = rules[r].GetPriorPosition(position)
    z = position
    
    a = ((y - z) * modinv(x - y, N)) % N
    b = (y - a*x) % N
    print(a, b)
    print((pow(a, iterations, N) * x + b * (pow(a, iterations, N) - 1) * modinv(a - 1, N))%N)
           
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
