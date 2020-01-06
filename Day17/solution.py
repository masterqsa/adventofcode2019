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
    maxx = -9999
    maxy = -9999
    vms = [VM(nums, [])]
    sched = Scheduler(vms)
    sched.connect(0, Scheduler.OUT)
    out = sched.run()
    s = ""
    x = 0
    y = 0
    while(len(out)>0):
        r = out.pop(0)
        if r == 10:
            print(s)
            maxy = max(maxy, y)
            y+=1
            x = 0
            s = ""
        else:
            s += chr(r)
            map[(x, y)] = chr(r)
            maxx = max(maxx, x)
            x += 1
    print(s)
    
    sum = 0
    for x in range(1, maxx):
        for y in range(1, maxy):
            if map[(x,y)] == '#' and map[(x-1, y)] == '#' and map[(x+1, y)] == '#' and map[(x, y-1)] == '#' and map[(x, y+1)] == '#':
                sum += x * y
    print(sum)

    #Part 2
    nums[0] = 2
    for x in range(1, maxx):
        for y in range(0, maxy):
            if map[(x,y)] == '^':
                r_x = x
                r_y = y
    
    print(r_x, r_y)
    x = r_x
    y = r_y
    visited = set()
    visited.add((r_x, r_y))
    sequence = list()
    prev = 'X'
    def Direction(prev):
        if prev == 'L':
            return (-1, 0)
        elif prev == 'R':
            return (1, 0)
        elif prev == 'U':
            return (0, -1)
        elif prev == 'D':
            return (0, 1)
        else:
            return (0, 0)
    while(True):
        dx, dy = Direction(prev)
        if x+dx > 0 and x+dx <= maxx and y+dy >= 0 and y+dy < maxy and map[(x+dx, y+dy)] == '#':
            sequence.append((prev, 1))
            x+=dx
            y+=dy
        elif x > 0 and ((x-1,y) not in visited or prev == 'L') and map[(x-1, y)] == '#':
            sequence.append(('L', 1))
            prev = 'L'
            x-=1
        elif x < maxx and ((x+1,y) not in visited or prev == 'R') and map[(x+1, y)] == '#':
            sequence.append(('R', 1))
            prev = 'R'
            x+=1
        elif y > 0 and ((x,y-1) not in visited or prev == 'U') and map[(x, y-1)] == '#':
            sequence.append(('U', 1))
            prev = 'U'
            y-=1
        elif y < maxy-1 and ((x,y+1) not in visited  or prev == 'D') and map[(x, y+1)] == '#':
            sequence.append(('D', 1))
            prev = 'D'
            y+=1
        else:
            break
        visited.add((x,y))
    print(sequence)
    prev = 'X'
    count = 0
    commands = list()
    for s in sequence:
        if s[0] == prev:
            count+=1
        else:
            if prev != 'X':
                commands.append((prev, count))
            prev = s[0]
            count = 1
    commands.append((prev, count))
    print(commands)
    com = list()
    com.append(commands[0])
    for i in range(1, len(commands)):
        if (commands[i][0] == 'U' and commands[i-1][0]=='L') or (commands[i][0] == 'R' and commands[i-1][0]=='U') or(commands[i][0] == 'D' and commands[i-1][0]=='R') or(commands[i][0] == 'L' and commands[i-1][0]=='D'):
            com.append(('R', commands[i][1]))
        else:
            com.append(('L', commands[i][1]))
    print(com)
    
    vms = [VM(nums, [])]
    sched = Scheduler(vms)
    sched.connect(0, Scheduler.OUT)
        
    steps = 'A,C,A,C,B,B,C,A,C,B'
    A = 'L,8,R,12,R,12,R,10'
    B = 'L,10,R,10,L,6'
    C = 'R,10,R,12,R,10'
    n = 'n'    

    for s in [steps, A, B, C, n]:
        for c in s + "\n":
            vms[0].push_in([ord(c)])
    
    out = sched.run()
    print(out)
    
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
