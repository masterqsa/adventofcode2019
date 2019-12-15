import sys; sys.dont_write_bytecode = True; from utils import *


def is_valid(num: int) -> bool:
    secure_doubles = False
    doubles = False
    doubles_i = -1
    a = str(num)
    prev = a[0]
    for i in range(1, 6):
        if a[i] == prev:
            doubles = True
            doubles_i = i
            if i > 1 and a[i-2] == a[i]:
                doubles = False
                doubles_i = -1
        elif doubles:
            secure_doubles = True

        if a[i] < prev:
            return False
        prev = a[i]
    return secure_doubles or doubles



def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    lines = inp.splitlines()
    line = lines[0].split('-')
    a = int(line[0])
    b = int(line[1])
    count = 0
    for i in range(a, b+1):
        if is_valid(i):
            count+=1
                
    #print(dist)
    print(count)
    
    
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



run_samples_and_actual([
# Part 1
r"""123789-123799
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
