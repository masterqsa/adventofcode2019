import sys; sys.dont_write_bytecode = True; from utils import *
import time
import os
import queue

POSITION = 0
IMMEDIATE = 1
RELATIVE = 2

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
RELATIVE_BASE_OFFSET = 9
HALT = 99

READ = 0
WRITE = 1

def op(op_code: int, a: int, b: int):
    if op_code == ADD:
        return a + b
    else:
        return a * b
    
def codeop(op_code: int):
    op = op_code % 100
    mode1 = (int)(op_code / 100) % 10
    mode2 = (int)(op_code / 1000) % 10
    mode3 = (int)(op_code / 10000) % 10
    return op, mode1, mode2, mode3

class VM:
    def __init__(self, code, input=None):
        self.mem = defaultdict(int)
        for i in range(len(code)):
            self.mem[i] = code[i]
        self.inp = deque([] if input is None else input)
        self.out = []
    def __getitem__(self, index):
        return self.mem[index]

    def __setitem__(self, index, val):
        self.mem[index] = val
    
    def push_in(self, inp):
        self.inp.extend(inp)
    
    def pop_out(self):
        out = self.out
        self.out = []
        return out
    
    def par(self, pos: int, mode: int):
        return self[self[pos]] if mode == POSITION else (self[pos] if mode == IMMEDIATE else self[self.relativeBase + self[pos]])
    
    def run(self):
        self.cur = 0
        self.relativeBase = 0
        exit = False
        while not exit:
            oper, mode1, mode2, mode3 = codeop(self[self.cur])
            if oper == IN:
                while not self.inp:
                    yield
                if mode1 == POSITION:
                    self[self[self.cur+1]] = self.inp.popleft()
                elif mode1 == RELATIVE:
                    self[self.relativeBase + self[self.cur+1]] = self.inp.popleft()
                self.cur += 2
            elif oper == HALT:
                exit = True
            elif oper == OUT:
                self.out.append(self.par(self.cur+1, mode1))
                self.cur += 2
            elif oper == ADD:
                val = self.par(self.cur+1, mode1) + self.par(self.cur+2, mode2)
                if mode3 == POSITION:
                    self[self[self.cur + 3]] = val
                elif mode3 == RELATIVE:
                    self[self.relativeBase + self[self.cur + 3]] = val
                self.cur += 4
            elif oper == MUL:
                val = self.par(self.cur+1, mode1) * self.par(self.cur+2, mode2)
                if mode3 == POSITION:
                    self[self[self.cur + 3]] = val
                elif mode3 == RELATIVE:
                    self[self.relativeBase + self[self.cur + 3]] = val
                self.cur += 4
            elif oper == JUMP_TRUE:
                if self.par(self.cur+1, mode1) != 0:
                    self.cur = self.par(self.cur+2, mode2)
                else:
                    self.cur += 3
            elif oper == JUMP_FALSE:
                if self.par(self.cur+1, mode1) == 0:
                    self.cur = self.par(self.cur+2, mode2)
                else:
                    self.cur += 3
            elif oper == LESS_THAN:
                val = 1 if (self.par(self.cur+1, mode1) < (self.par(self.cur+2, mode2))) else 0
                if mode3 == POSITION:
                    self[self[self.cur + 3]] = val
                elif mode3 == RELATIVE:
                    self[self.relativeBase + self[self.cur + 3]] = val
                self.cur += 4
            elif oper == EQUALS:
                val = 1 if (self.par(self.cur+1, mode1) == (self.par(self.cur+2, mode2))) else 0
                if mode3 == POSITION:
                    self[self[self.cur + 3]] = val
                elif mode3 == RELATIVE:
                    self[self.relativeBase + self[self.cur + 3]] = val
                self.cur += 4
            elif oper == RELATIVE_BASE_OFFSET:
                self.relativeBase += self.par(self.cur+1, mode1)
                self.cur += 2
    
class Scheduler:
    OUT = object()

    def __init__(self, vms):
        self.vms = vms
        self.connections = [[] for _ in vms]
        self.waiting = deque(range(len(self.vms)))
        self.gens = [vm.run() for vm in self.vms]
        self.out = []
    
    def connect(self, start, end):
        self.connections[start].append(end)

    def run(self):
        while self.waiting:
            curr = self.waiting.popleft()

            try:
                next(self.gens[curr])
                self.waiting.append(curr)
            except StopIteration:
                pass

            out = self.vms[curr].pop_out()
            for conn in self.connections[curr]:
                if conn is Scheduler.OUT:
                    self.out.extend(out)
                    return self.out
                else:
                    self.vms[conn].push_in(out)
        
        return self.out



def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    nums = ints(inp)
    map = defaultdict()
    maxx = 0
    maxy = 0
    # vms = [VM(nums, [])]
    # sched = Scheduler(vms)
    # sched.connect(0, Scheduler.OUT)
    # vms[0].push_in([0,0])
    # out = sched.run()
    # print(out)
    sum = 0
    minRatio = 2
    maxRatio = 0
    for x in range(0, 50):
        for y in range(0,50):
            vms = [VM(nums, [x,y])]
            sched = Scheduler(vms)
            sched.connect(0, Scheduler.OUT)
            out = sched.run()
            #print(out)
            if out.pop() == 1:
                sum+=1
                map[(x,y)] = '#'
                if x > 20 and y > 40:
                    if x/float(y) > maxRatio:
                        maxRatio = x/float(y)
                    if x/float(y) < minRatio:
                        minRatio = x/float(y)
            else:
                map[(x,y)] = '.'
    print(sum)
    for y in range(0, 50):
        s=""
        for x in range(0,50):
            s=s+map[(x,y)]
        print(s)
    print(minRatio, maxRatio)
    # minRatio += 0.3
    # maxRatio -= 0.3
    print("***********")
    seen = set()
    x_from = 680
    x_to = x_from + 100
    for x in range(x_from, x_to):
        #print(int(-2 + x/maxRatio),int(3 + x/minRatio))
        count = 0
        for y in range(int(3 + x/minRatio),int(-2 + x/maxRatio),-1):
            #print(x,y)
            vms = [VM(nums, [x,y])]
            sched = Scheduler(vms)
            sched.connect(0, Scheduler.OUT)
            out = sched.run()
            #print(out)
            if out.pop() == 1:
                map[(x,y)] = '#'
                if x/float(y) > maxRatio:
                    maxRatio = x/float(y)
                if x/float(y) < minRatio:
                    minRatio = x/float(y)
                #print(x,y)
                if count < 3:
                    seen.add((x+99, y-99))
                    count+=1
                else:
                    break
            else:
                count = 0
                map[(x,y)] = '.'
    print(minRatio, maxRatio)
    minRatio = 0.567741935483871
    maxRatio = 0.704
    #print(seen)
    
    for x in range(x_from + 100, x_to + 100):
        count = 0
        #print(int(-2 + x/maxRatio),int(3 + x/minRatio))
        for y in range(int(-2 + x/maxRatio),int(3 + x/minRatio)):
            vms = [VM(nums, [x,y])]
            sched = Scheduler(vms)
            sched.connect(0, Scheduler.OUT)
            out = sched.run()
            #print(out)
            if out.pop() == 1:
                map[(x,y)] = '#'
                if x/float(y) > maxRatio:
                    maxRatio = x/float(y)
                if x/float(y) < minRatio:
                    minRatio = x/float(y)
                if (x,y) in seen:
                    print(x,y)
                count += 1
                if count > 3:
                    break
                #print(x,y)
            else:
                map[(x,y)] = '.'
    print(minRatio, maxRatio)
    
    # for y in range(1270, 1385):
    #     s = ""
    #     for x in range(x_from, x_to+150):
    #         if (x,y) in map:
    #             s += map[(x,y)]
    #         else:
    #             s += "?"
            
    #     print(s)
    #7081147
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
