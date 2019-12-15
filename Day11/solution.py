import sys; sys.dont_write_bytecode = True; from utils import *

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
    x, y = 0, 0
    dx, dy = 0, -1
    
    def turnRight(dx: int, dy: int):
        if dx == 0 and dy == -1:
            return 1, 0
        if dx == 1 and dy == 0:
            return 0, 1
        if dx == 0 and dy == 1:
            return -1, 0
        if dx == -1 and dy == 0:
            return 0, -1
    def turnLeft(dx: int, dy: int):
        if dx == 0 and dy == -1:
            return -1, 0
        if dx == 1 and dy == 0:
            return 0, -1
        if dx == 0 and dy == 1:
            return 1, 0
        if dx == -1 and dy == 0:
            return 0,  1
        
    vms = [VM(nums, [])]
    sched = Scheduler(vms)
    sched.connect(0, Scheduler.OUT)
    exit = False
    map[(0,0)] = 1
    minX = 99999999
    maxX = -99999999
    minY = 99999999
    maxY = -99999999
    while exit == False:   
        val = 0 if (x,y) not in map else map[(x,y)]
        vms[0].push_in([val])
        out = sched.run()
        if len(out) == 2:
            map[(x,y)] = sched.out.pop(0)
            if sched.out.pop(0) == 0:
                dx, dy = turnLeft(dx, dy)
            else:
                dx, dy = turnRight(dx, dy)
            x += dx
            y += dy  
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)
        else:
            exit = True
    for j in range(minY, maxY+1):
        s=""
        for i in range(minX, maxX+1):
            s+=' ' if (i,j) not in map or map[(i,j)] == 0 else '*'
        print(s)
    
    print(len(map))
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
