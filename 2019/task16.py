from itertools import cycle, repeat
import numpy as np

with open('puzzle_input/input16.txt') as file:
    puzzle_input = [int(x) for x in str(file.read())]

def FFT(input_list, offset = 0):
    global base_pattern
    first_digits = None
    for _ in range(100):
        output = []
        for i in range(0, len(input_list)):
            new_pattern = [x for x in base_pattern for y in repeat(x, i + 1)]
            pattern_cycle = cycle(new_pattern)
            next(pattern_cycle)
            new_digit = 0
            for x in input_list:
                new_digit += (x * next(pattern_cycle))
            output.append(int(str(new_digit)[-1]))
        input_list = output
        final_digits = ''.join(map(str, output[offset : 8 + offset]))
    return final_digits

base_pattern = [0, 1, 0, -1]

real_signal = puzzle_input * 10000
offset = puzzle_input[:7]

print('Part 1:', FFT(puzzle_input.copy()))
print('Part 2:', FFT(real_signal, offset))