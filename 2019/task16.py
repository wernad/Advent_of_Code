from itertools import cycle, repeat

with open('puzzle_input/input16.txt') as file:
    puzzle_input = list(map(int,file.read()))

def FFT(input_list, offset = 0):
    global base_pattern
    for j in range(100):
        output = []
        for i in range(0, len(input_list)):
            new_pattern = [x for x in base_pattern for y in repeat(x, i + 1)]
            pattern_cycle = cycle(new_pattern)
            next(pattern_cycle)
            new_digit = sum([x * next(pattern_cycle) for x in input_list])
            if new_digit >= 0:
                input_list[i] = new_digit % 10
            else:
                input_list[i] = (-new_digit) % 10
    return input_list[:8]

def FFT_offset(input_list, offset):
    global base_pattern
    input_list = input_list[offset:]
    for j in range(100):
        partial_sum = 0
        for i in range(len(input_list)-1, -1, -1):
            partial_sum += input_list[i]
            
            if partial_sum >= 0:
                input_list[i] = partial_sum % 10
            else:
                input_list[i] = (-partial_sum) % 10
    return input_list[:8]

base_pattern = [0, 1, 0, -1]

real_signal = puzzle_input * 10000
offset = int(''.join(map(str, puzzle_input[:7])))

print('Part 1:', ''.join([str(x) for x in FFT(puzzle_input.copy())]))
print('Part 2:', ''.join([ str(x) for x in FFT_offset(real_signal, offset)]))