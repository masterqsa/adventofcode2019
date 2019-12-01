import sys; sys.dont_write_bytecode = True; from utils import *

# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

def calc_fuel(mass: int):
    return math.floor(mass / 3) - 2

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    total = 0
    lines = inp.splitlines()
    for s in lines:
        i = int(s)
        f = calc_fuel(i)
        total += f
        more_mass = f
        while more_mass > 6:
            more_mass = calc_fuel(more_mass)
            total += more_mass
    
    
    
    print(total)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""12
14
1969
100756
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
