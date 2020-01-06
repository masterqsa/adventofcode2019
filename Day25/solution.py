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
    
    def run_command(self, command):
        for c in command + "\n":
            self.vms[0].push_in([ord(c)])
    
        return self.run()

class Room:
    def __init__(self, name, doors, items, ejected = 0):
        self.name = name
        self.doors = doors
        self.items = items
        self.options = deque(doors)
        self.ejected = ejected #0 - None, 1 = Underweight, 2 = Overweight
    
    def take(self, item):
        self.items.remove(item)
        
    def drop(self, item):
        self.items.add(item)
    
    def deadend(self):
        return True if len(self.options) == 0 else False
    
    def explore(self):
        return self.options.pop()

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    nums = ints(inp)
    
    vms = [VM(nums, [])]
    sched = Scheduler(vms)
    sched.connect(0, Scheduler.OUT)
    
    directions = defaultdict()
    directions["north"] = (0,-1)
    directions["south"] = (0,1)
    directions["west"] = (-1,0)
    directions["east"] = (1,0)
    
    def opposite(dir):
        if dir == "north":
            return "south"
        if dir == "south":
            return "north"
        if dir == "west":
            return "east"
        if dir == "east":
            return "west"
        
        
    #north south west east
    #take x
    #drop x
    
    commands = ['north', 'take festive hat','east', 'take prime number','west','south','east','north', 'drop prime number', 'north', 'south', 'inv'] 
    commands = ['inv']  
    
    # == Warp Drive Maintenance ==
    # It appears to be working normally.
    #Items here:
    # - weather machine
    # - prime number
    #Doors here lead:
    # - north
    # - south
    #Items in your inventory:
    # - festive hat
    #You drop the prime number.  
    #Command? 
    
    # for s in commands:
    #     for c in s + "\n":
    #         vms[0].push_in([ord(c)])
    
    #     out = sched.run()
    #     s=""
    #     #print(out)
    #     while len(out)> 0:
    #         c = chr(out.pop(0))
    #         if c == '\n':
    #             print(s)
    #             s = ""
    #         else:
    #             s += c 
    
    out = sched.run()
    s=""
    #print(out)
    while len(out)> 0:
        c = chr(out.pop(0))
        if c == '\n':
            print(s)
            s = ""
        else:
            s += c
    start_coord = (0,0)
    start_room = "== Hull Breach =="
    start_doors = {"north","east","south"}

    map = defaultdict()
    map[start_coord] = Room(start_room, start_doors, {})
    rooms = defaultdict()
    rooms[start_room] = start_coord
    history = deque()
    inv = set()
    
    def ParseOut(out):
        name = ""
        descr = ""
        doors = list()
        items = list()
        doors_started = False
        items_started = False
        name_started = False
        ejected = 0
        cantgo = False
        room = Room("BAD", doors, items, ejected)
        s = ""
        while len(out)> 0:
            c = chr(out.pop(0))
            if c == '\n':
                print(s)
                if len(s)> 0 and s[0] == '=':
                    #room name
                    name = s
                    doors = list()
                    items = list()
                    name_started = True
                elif s=="":
                    items_started = False
                    doors_started = False
                    name_started = False
                elif name_started:
                    descr = s
                    name_started = False
                elif doors_started:
                    doors.append(s[2:])
                elif items_started:
                    items.append(s[2:])
                elif s=="Doors here lead:":
                    doors_started = True
                elif s=="Items here:":
                    items_started = True
                elif s=="Command?":
                    room = Room(name, doors, items, ejected)
                elif s=="You can't go that way.":
                    raise Exception(s)
                elif len(s) > 13 and s[0:8] == "You take":
                    inv.add(s[13:-1])
                    print(s)
                elif len(s) > 13 and s[0:8] == "You drop":
                    inv.remove(s[13:-1])
                    print(s)
                elif s=="A loud, robotic voice says \"Alert! Droids on this ship are heavier than the detected value!\" and you are ejected back to the checkpoint.":
                    ejected = 1
                elif s=="A loud, robotic voice says \"Alert! Droids on this ship are lighter than the detected value!\" and you are ejected back to the checkpoint.":
                    ejected = 2
                elif s=="It is suddenly completely dark! You are eaten by a Grue!":
                    raise Exception(s)
                elif s=="The giant electromagnet is stuck to you.  You can't move!!":
                    raise Exception(s)
                else:
                    #unusual
                    print(s)
                s = ""
            else:
                s += c
        return room

    
    def GoBack():
        global x
        global y
        last_step = history.pop()
        return_step = opposite(last_step)
        out = sched.run_command(return_step)
        diff = directions[return_step]
        x+=diff[0]
        y+=diff[1]
        room = ParseOut(out)
        if room.ejected:
            history.append(last_step)
    
    def EnterRoom(direction):
        global x
        global y
        history.append(direction)
        diff = directions[direction]
        x+=diff[0]
        y+=diff[1]
        out = sched.run_command(direction)
        room = ParseOut(out)
        if room.name in rooms:
            (x, y) = rooms[room.name]
        else:
            rooms[room.name] = (x,y)
        map[(x,y)] = room
        if room.ejected in [1,2]:
            history.pop()
            room.options.appendleft(direction)
        return room
    
    def TryPickup(room):
        bad_items = ["molten lava","giant electromagnet","photons","molten lava","escape pod","infinite loop"]
        for i in bad_items:
            if i in room.items:
                room.items.remove(i)
            
        if len(room.items) > 0:
            command = "take "+room.items[0]
            out = sched.run_command(command)
            room = ParseOut(out)
            return True
        else:
            return False
    
    def TryDrop(inv):
        if len(inv) > 0:
            command = "drop "+next(iter(inv))
            out = sched.run_command(command)
            room = ParseOut(out)
            return True
        return False
    
    global x
    global y
    x = 0
    y = 0
    step = 0
    while step < 100:
        step+=1
        if map[(x,y)].deadend():
            print("Dead end, going back from", x, y)
            GoBack()
        else:
            new_direction = map[(x,y)].explore()
            if len(history)>0:
                while new_direction == opposite(history[len(history)-1]) and not map[(x,y)].deadend():
                    new_direction = map[(x,y)].explore()
            if len(history)>0 and new_direction == opposite(history[len(history)-1]):
                print("Dead end, going back from", x, y)
                GoBack()
            else:
                #expoloring new room
                print("Exploring room to the", new_direction)
                room = EnterRoom(new_direction)
                if room.ejected == 1: #underweight
                    res = TryPickup(room)
                elif room.ejected == 0:
                    res = TryPickup(room)
                elif room.ejected == 2:
                    res = TryDrop(inv)
                print("Room is", room.name)
    # for s in commands:
    #     for c in s + "\n":
    #         vms[0].push_in([ord(c)])
    
    #     out = sched.run()
    #     s=""
    #     #print(out)
    #     for c in [chr(x) for x in out]:
    #         if c == '\n':
    #             print(s)
    #             s = ""
    #         else:
    #             s += c
    print(map)
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
