import sys; sys.dont_write_bytecode = True; from utils import *


def op(op_code: int, a: int, b: int):
    if op_code == 1:
        return a + b
    else:
        return a * b
    
def codeop(op_code: int):
    op = op_code % 100
    mode1 = (int)(op_code / 100) % 10
    mode2 = (int)(op_code / 1000) % 10
    mode3 = (int)(op_code / 10000) % 10
    return op, mode1, mode2, mode3


def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    nums = ints(inp)
    input_params = []
    input_params.append(5)
    cur = 0
    # if nums[0] == 3:
    #     nums[nums[1]] = input_param
    #     cur = 2
    def par(pos: int, mode: int) -> int:
        return nums[nums[pos]] if mode == 0 else nums[pos]
        
    exit = False
    while not exit:
        oper, mode1, mode2, mode3 = codeop(nums[cur])
        if oper == 3:
            nums[nums[cur+1]] = input_params.pop()
            cur += 2
        elif oper == 99:
            exit = True
        elif oper == 4:
            print(par(cur+1, mode1))
            cur += 2
        elif oper in range(1,3):
            nums[nums[cur + 3]] = op(oper, par(cur+1, mode1), par(cur+2, mode2))
            cur += 4
        elif oper == 5:
            if par(cur+1, mode1) != 0:
                cur = par(cur+2, mode2)
            else:
                cur += 3
        elif oper == 6:
            if par(cur+1, mode1) == 0:
                cur = par(cur+2, mode2)
            else:
                cur += 3
        elif oper == 7:
            nums[nums[cur + 3]] = 1 if (par(cur+1, mode1) < (par(cur+2, mode2))) else 0
            cur += 4
        elif oper == 8:
            nums[nums[cur + 3]] = 1 if (par(cur+1, mode1) == (par(cur+2, mode2))) else 0
            cur += 4
    
    
    
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""3,9,8,9,10,9,4,9,99,-1,8
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
