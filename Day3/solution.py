import sys; sys.dont_write_bytecode = True; from utils import *

def vector_mult(ax: int,ay: int,bx: int, by: int) -> int:
    return ax*by-bx*ay

class equation:
    def __init__(self, x1: int,y1: int,x2: int, y2: int) -> None:
        self.A=y2-y1                                         
        self.B=x1-x2
        self.C=-x1*(y2-y1)+y1*(x2-x1)

class interval:
    def __init__(self, x1: int,y1: int,x2: int, y2: int, d: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.steps = d
    def intersects(self, b) -> bool:
        v1 = vector_mult(b.x2 - b.x1, b.y2 - b.y1, self.x1 - b.x1, self.y1 - b.y1)
        v2 = vector_mult(b.x2 - b.x1, b.y2 - b.y1, self.x2 - b.x1, self.y2 - b.y1)
        v3 = vector_mult(self.x2 - self.x1, self.y2 - self.y1, b.x1 - self.x1, b.y1 - self.y1)
        v4 = vector_mult(self.x2 - self.x1, self.y2 - self.y1, b.x2 - self.x1, b.y2 - self.y1)
        if (v1*v2)<0 and (v3*v4)<0:
            return True
        return False
    def intersection(self, b) -> (int, int):
        eq1 = equation(self.x1, self.y1, self.x2, self.y2)
        eq2 = equation(b.x1, b.y1, b.x2, b.y2)
        d=(eq1.A*eq2.B-eq1.B*eq2.A)
        dx=(-eq1.C*eq2.B+eq1.B*eq2.C)
        dy=(-eq1.A*eq2.C+eq1.C*eq2.A)
        x=(dx/d)
        y=(dy/d)
        return (x,y)
    def intersection_steps(self, b) -> int:
        (x, y) = self.intersection(b)
        steps = abs(self.x1 - x) + abs(self.y1 - y) + abs(b.x1 - x) + abs(b.y1 - y) + self.steps + b.steps
        return steps

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    map = list()
    x, y = 0, 0
    steps = 0
    for step in lines[0].split(','):
        d = step[0]
        n = int(step[1:])
        dx, dy = 0, 0
        if d == 'R':
            dx+=n
        elif d == 'L':
            dx-=n
        elif d == 'U':
            dy-=n
        elif d == 'D':
            dy+=n
        map.append(interval(x, y, x+dx, y+dy, steps))
        x+=dx
        y+=dy
        steps += (abs(dx) + abs(dy))
    dist = 9223372036854775807
    beststeps = 9223372036854775807
    x, y = 0, 0
    steps = 0
    for step in lines[1].split(','):
        d = step[0]
        n = int(step[1:])
        dx, dy = 0, 0
        if d == 'R':
            dx+=n
        elif d == 'L':
            dx-=n
        elif d == 'U':
            dy-=n
        elif d == 'D':
            dy+=n
        o = interval(x, y, x+dx, y+dy, steps)
        x+=dx
        y+=dy
        for m in map:
            if o.intersects(m):
                # (i, j) = o.intersection(m)
                # if dist > abs(i) + abs(j):
                #     dist = abs(i) + abs(j)
                ds = o.intersection_steps(m)
                if ds < beststeps:
                    beststeps = ds
        steps += (abs(dx) + abs(dy))
                
    #print(dist)
    print(beststeps)
    
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
""",r"""R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
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
