import sys; sys.dont_write_bytecode = True; from utils import *

POSITION = 0
IMMEDIATE = 1

ADD = 1
MUL = 2
IN = 3
OUT = 4
JUMP_TRUE = 5
JUMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
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
        self.mem = list(code)
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
        return self[self[pos]] if mode == POSITION else self[pos]
    
    def run(self):
        self.cur = 0
        exit = False
        while not exit:
            oper, mode1, mode2, mode3 = codeop(self[self.cur])
            if oper == IN:
                while not self.inp:
                    yield
                self[self[self.cur+1]] = self.inp.popleft()
                self.cur += 2
            elif oper == HALT:
                exit = True
            elif oper == OUT:
                self.out.append(self.par(self.cur+1, mode1))
                self.cur += 2
            elif oper == ADD:
                self[self[self.cur + 3]] = self.par(self.cur+1, mode1) + self.par(self.cur+2, mode2)
                self.cur += 4
            elif oper == MUL:
                self[self[self.cur + 3]] = self.par(self.cur+1, mode1) * self.par(self.cur+2, mode2)
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
                self[self[self.cur + 3]] = 1 if (self.par(self.cur+1, mode1) < (self.par(self.cur+2, mode2))) else 0
                self.cur += 4
            elif oper == EQUALS:
                self[self[self.cur + 3]] = 1 if (self.par(self.cur+1, mode1) == (self.par(self.cur+2, mode2))) else 0
                self.cur += 4
    
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
                else:
                    self.vms[conn].push_in(out)
        
        return self.out



def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    nums = ints(inp)
    
    
    permutations = []
    def permute(a, l, r): 
        if l==r: 
            permutations.append(a.copy()) 
        else: 
            for i in range(l,r+1): 
                a[l], a[i] = a[i], a[l] 
                permute(a, l+1, r) 
                a[l], a[i] = a[i], a[l]
    # grand_max = 0
    
    # permute(list(range(5)), 0, 4)
    # for seq in permutations:
    #     vms = [VM(nums, [p]) for p in seq]
    #     vms[0].push_in([0])
    #     sched = Scheduler(vms)
    #     for i in range(4):
    #         sched.connect(i, i+1)
    #     sched.connect(4, Scheduler.OUT)

    #     out = sched.run()
    #     grand_max = max(grand_max, out[-1])
    # print(grand_max)
    
      
    grand_max = 0  
    permute(list(range(5, 10)), 0, 4)
    for seq in permutations:
        vms = [VM(nums, [p]) for p in seq]
        vms[0].push_in([0])
        sched = Scheduler(vms)
        for i in range(4):
            sched.connect(i, i+1)
        sched.connect(4, 0)
        sched.connect(4, Scheduler.OUT)

        out = sched.run()
        grand_max = max(grand_max, out[-1])
        
    
    print(grand_max)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
""",r"""
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

"""],[
# Part 2
r"""3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
