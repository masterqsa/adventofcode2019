import sys; sys.dont_write_bytecode = True; from utils import *
import queue
import math

class SequenceGenerator:
    def __init__(self, pos: int):
        self.mods = [0, 1, 0, -1]
        self.pos=pos
        self.current = 0
        self.iter = 1
    def get(self):
        while True:
            if self.iter > self.pos:
                self.current += 1
                self.iter = 0
                if self.current > 3:
                    self.current = 0
            self.iter += 1
            yield self.mods[self.current]

def do_case(inp: str, sample=False):
    lines = inp.splitlines()
    l1 = list()
    
    for c in lines[0]:
        l1.append(int(c))
    # for _ in range(0, 100):
    #     l2 = list()
    #     for i in range(0, len(l1)):
    #         s = 0
    #         sg = SequenceGenerator(i)
    #         gen = sg.get()
    #         for j in range(0, len(l1)):
    #             k = next(gen)
    #             s = (s + l1[j] * k)
    #         l2.append(abs(s) % 10)
    #     l1 = l2
    #     #print(l1)
    #     # sg = SequenceGenerator(3)
    #     # gen = sg.get()
    #     # for i in range(0, 15):
    #     #     print(next(gen))
    # print(''.join(str(l1[i]) for i in range(0,min(8, len(l1)))))
        
    #part 2
    skip = 0
    for i in range(0,7):
        skip = skip * 10+l1[i]
    l1 = (l1*10000)[skip:]
    #skip = 5976277
        
    for _ in range(100):
        # accumulate backwards
        rev_partial_sum = l1[-1:]
        for x in l1[-2::-1]:
        # for x in reversed(l[:-1]):
            rev_partial_sum.append(rev_partial_sum[-1]+x)
        l1 = [abs(x)%10 for x in reversed(rev_partial_sum)]
        
    print(''.join([str(l1[i]) for i in range(0, 8)]))
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""12345678
""",r"""80871224585914546619083218645595
""",r"""19617804207202209144916044189917
""",r"""69317163492948606335995924319873
""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r"""03036732577212944063491565474664
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
