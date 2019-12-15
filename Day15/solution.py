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
    map[(0,0)] = 1
    d = defaultdict()
    d[1] = (0, -1)
    d[2] = (0, 1)
    d[3] = (-1, 0)
    d[4] = (1, 0)
    #north (1), south (2), west (3), and east (4)
    # 0: The repair droid hit a wall. Its position has not changed.
    # 1: The repair droid has moved one step in the requested direction.
    # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
    os_x = None
    os_y = None
    minx = 9999
    maxx = -9999
    miny = 9999
    maxy = -9999
    x = 0
    y = 0
    stack = []
    vms = [VM(nums, [])]
    sched = Scheduler(vms)
    sched.connect(0, Scheduler.OUT)
    reply = None
    stack.append((0, range(1,6)))
    def getbacktrack(dir):
        if dir == 1:
            return 2
        elif dir == 2:
            return 1
        elif dir == 3:
            return 4
        else:
            return 3
        
    while(len(stack)>0):
        backtrack, options = stack.pop()
        for dir in options:
            if dir == 5: #need to backtrack
                vms[0].push_in([backtrack])
                out = sched.run()
                if len(out) == 0:
                    break
                reply = out.pop(0)
                dx, dy = d[backtrack]
                x+=dx
                y+=dy
            else:
                dx, dy = d[dir]
                if (x+dx, y+dy) in map:
                    continue
                vms[0].push_in([dir])  
                out = sched.run()
                if len(out) == 0:
                    break
                reply = out.pop(0)
                maxx = max(maxx, x+dx)
                minx = min(minx, x+dx)
                maxy = max(maxy, y+dy)
                miny = min(miny, y+dy)
                if reply == 0:
                    map[(x+dx, y+dy)] = 0
                elif reply == 1:
                    x+=dx
                    y+=dy
                    map[(x,y)] = 1
                    stack.append((backtrack, range(dir+1,6)))
                    stack.append((getbacktrack(dir), range(1,6)))
                    break
                elif reply == 2:
                    x+=dx
                    y+=dy
                    map[(x,y)] = 2
                    os_x = x
                    os_y = y
                    stack.append((backtrack, range(dir+1,6)))
                    stack.append((getbacktrack(dir), range(1,6)))
                    break
            
    for j in range(miny, maxy+1):
        s = ""
        for i in range(minx, maxx+1):
            if (i,j) in map:
                if map[(i,j)] == 0:
                    s+="#"
                elif map[(i,j)] == 1:
                    s+="."
                elif map[(i,j)] == 2:
                    s+="x"
            else:
                s+=" "
        print(s)
    x, y = 0, 0
    visited = defaultdict()
    visited[(0,0)] = 0
    q = queue.Queue()
    q.put((x,y))
    while q.qsize() > 0:
        cur = q.get()
        for dir in d:
            dx,dy = d[dir]
            x = cur[0]+dx
            y = cur[1]+dy
            if (x,y) not in visited and map[(x, y)] > 0:
                q.put((x,y))
                visited[(x,y)] = visited[(cur[0],cur[1])] + 1
                
        if (x, y) == (os_x, os_y):
            break
    
    print(visited[(os_x, os_y)])
    
    visited = defaultdict()
    visited[(os_x, os_y)] = 0
    q.put((os_x, os_y))
    max_dist = 0
    while q.qsize() > 0:
        cur = q.get()
        for dir in d:
            dx,dy = d[dir]
            x = cur[0]+dx
            y = cur[1]+dy
            if (x,y) not in visited and map[(x, y)] > 0:
                q.put((x,y))
                visited[(x,y)] = visited[(cur[0],cur[1])] + 1
                max_dist = max(max_dist, visited[(x,y)])
    print(max_dist)
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
