import sys; sys.dont_write_bytecode = True; from utils import *


def do_case(inp: str, sample=False):
    # READ THE PROBLEM FROM TOP TO BOTTOM OK
    layer_size = 25 * 6
    layers = (int)(len(inp) / layer_size)
    # min_zeros = layer_size
    # min_zeros_index = 0
    # layer_ones = defaultdict(int)
    # layer_twos = defaultdict(int)
    # for l in range(0, layers):
    #     zeros = 0
    #     ones = 0
    #     twos = 0
    #     for i in range(0, layer_size):
    #         if inp[(l * layer_size) + i] == '0':
    #             zeros += 1
    #         elif inp[(l * layer_size) + i] == '1':
    #             ones += 1
    #         elif inp[(l * layer_size) + i] == '2':
    #             twos += 1
    #     if zeros < min_zeros:
    #         min_zeros = zeros
    #         min_zeros_index = l
    #     layer_ones[l] = ones
    #     layer_twos[l] = twos
    
    # print(layer_ones[min_zeros_index] * layer_twos[min_zeros_index])
    
    screen = [2]*layer_size
    for l in range(0, layers):
        for i in range(0, layer_size):
            if inp[(l * layer_size) + i] == '0':
                screen[i] = 0 if screen[i] == 2 else screen[i]
            elif inp[(l * layer_size) + i] == '1':
                screen[i] = 1 if screen[i] == 2 else screen[i]
    
    for i in range(0, 6):
        print(''.join([' ' if v==0 else '*' for v in screen[i*25:i*25+24]]))
            
    
        
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
