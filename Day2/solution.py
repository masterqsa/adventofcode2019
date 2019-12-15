import sys; sys.dont_write_bytecode = True; from utils import *

# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

def calc_fuel(mass: int):
    return math.floor(mass / 3) - 2

def op(op_code: int, a: int, b: int):
    if op_code == 1:
        return a + b
    else:
        return a * b

def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    nums = ints(inp)
    if len(nums) > 12:
        for i in range(0,99):
            for j in range(0,99):
                nums = ints(inp)
                if len(nums) > 12:
                    nums[1] = i
                    nums[2] = j
                cur = 0
                exit = False
                while not exit:
                    if nums[cur] == 99:
                        exit = True
                    else:
                        nums[nums[cur + 3]] = op(nums[cur], nums[nums[cur+1]], nums[nums[cur+2]])
                        cur += 4
                if nums[0] == 19690720:
                    print(i)
                    print(j)
    
    print(nums[0])
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""1,0,0,0,99
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
