import sys; sys.dont_write_bytecode = True; from utils import *
import queue

class moon:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.hidden = set()
    def kinetic(self):
        return abs(self.vx)+abs(self.vy)+abs(self.vz)
    def potential(self):
        return abs(self.x)+abs(self.y)+abs(self.z)
    def move(self):
        self.x+=self.vx
        self.y+=self.vy
        self.z+=self.vz

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    moons = list()
    for l in lines:
        m = ints(l)
        moons.append(moon(m[0], m[1], m[2]))
    n = len(moons)
    def hash_positions(mm):
        s=""
        for m in mm:
            s+=(str(m.x)+", "+str(m.y)+", "+str(m.z)+" / ")
        return s
    def gravity(a: moon, b:moon):
        if a.x > b.x:
            a.vx-=1
            b.vx+=1
        elif a.x < b.x:
            a.vx+=1
            b.vx-=1
        if a.y > b.y:
            a.vy-=1
            b.vy+=1
        elif a.y < b.y:
            a.vy+=1
            b.vy-=1
        if a.z > b.z:
            a.vz-=1
            b.vz+=1
        elif a.z < b.z:
            a.vz+=1
            b.vz-=1
    x_positions = defaultdict()
    y_positions = defaultdict()
    z_positions = defaultdict()
    sx, sy, sz="", "", ""
    for i in range(0, n):
        moons[i].move()
        sx+=(str(moons[i].x) + ","+ str(moons[i].vx) + ",")
        sy+=(str(moons[i].y) + ","+ str(moons[i].vy) + ",")
        sz+=(str(moons[i].z) + ","+ str(moons[i].vz) + ",")
    x_positions[sx] = 0
    y_positions[sy] = 0
    z_positions[sz] = 0
    cycle_x = 0
    cycle_y = 0
    cycle_z = 0
    for step in range(1,1000000):
        for i in range(0, n-1):
            for j in range(i, n):
                gravity(moons[i], moons[j])
        sx, sy, sz="", "", ""
        for i in range(0, n):
            moons[i].move()
            sx+=(str(moons[i].x) + "," + str(moons[i].vx) + ",")
            sy+=(str(moons[i].y) + "," + str(moons[i].vy) + ",")
            sz+=(str(moons[i].z) + "," + str(moons[i].vz) + ",")
        if cycle_x == 0 and sx in x_positions:
            cycle_x = step
            print(x_positions[sx])
        else:
            x_positions[sx] = step
        if cycle_y == 0 and sy in y_positions:
            cycle_y = step
            print(y_positions[sy])
        else:
            y_positions[sy] = step
        if cycle_z == 0 and sz in z_positions:
            cycle_z = step
            print(z_positions[sz])
        else:
            z_positions[sz] = step
        if cycle_x > 0 and cycle_y > 0 and cycle_z > 0:
            break
    
    print(cycle_x, cycle_y, cycle_z) # Part 2 answer is the least common multiple of these numbers
       
    #Part 1     
    # energy = 0
    # for i in range(0, n):
    #     energy += (moons[i].kinetic() * moons[i].potential())
    # print(energy)
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
r"""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""",r"""
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""], do_case)
