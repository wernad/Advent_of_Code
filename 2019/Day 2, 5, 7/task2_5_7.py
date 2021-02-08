import sys
from itertools import permutations 

if len(sys.argv) < 2:
    print('Missing argument. Please use number of day [2,5,7]')
    sys.exit()
args = sys.argv
if int(args[1]) not in {2,5,7}:
    print('Unknown argument(s). Please use number of day [2,5,7]')
    sys.exit()

with open('Day 2, 5, 7/input' + args[1] +'.txt') as file:
    puzzle_input = file.read()
    puzzle_input = puzzle_input.replace(',', ' ').split()
    puzzle_input = [int(i) for i in puzzle_input]

def process_intcode(puzzle_input, program_input):
    pi_copy = puzzle_input.copy()
    program_output = []
    i = 0
    j = 0
    while i <= len(pi_copy):
        opcode = str(pi_copy[i])
        param_modes = None
        if len(opcode) > 2:
            param_modes = opcode[:-2]
            opcode = opcode[-2:].lstrip('0')
        if opcode == '99':
            break
        elif opcode in {'1', '2', '5', '6', '7', '8'}:
            param_1, param_2 = None, None
            try:
                if param_modes[-1] == '0':
                    param_1 = pi_copy[pi_copy[i+1]]
                else:
                    param_1 = pi_copy[i+1]
            except (TypeError, IndexError):
                param_1 = pi_copy[pi_copy[i+1]]

            try:
                if param_modes[-2] == '0':
                    param_2 = pi_copy[pi_copy[i+2]]
                else:
                    param_2 = pi_copy[i+2]
            except (TypeError, IndexError):
                param_2 = pi_copy[pi_copy[i+2]]
            
            param_1, param_2 = int(param_1), int(param_2)

            if opcode == '1':
                pi_copy[pi_copy[i+3]] = param_1 + param_2
            elif opcode == '2':
                pi_copy[pi_copy[i+3]] = param_1 * param_2
            elif opcode == '5':
                i = param_2 if param_1 != 0 else i+3
                continue
            elif opcode == '6':
                i = param_2 if param_1 == 0 else i+3
                continue
            elif opcode == '7':
                pi_copy[pi_copy[i+3]] = 1 if param_1 < param_2 else 0
            elif opcode == '8':
                pi_copy[pi_copy[i+3]] = 1 if param_1 == param_2 else 0
            i += 4
        elif opcode == '3':
            pi_copy[pi_copy[i+1]] = program_input.pop(0) if len(program_input) > 1 else program_input[0]
            i += 2
        elif opcode == '4':
            program_output.append(pi_copy[pi_copy[i+1]])
            i += 2
        j += 1
    return pi_copy, program_output



#Task 5 Part 1 and Part 2
if int(args[1]) == 5:
    processed_input, program_output = process_intcode(puzzle_input, [1])
    print(program_output[-1])
    processed_input, program_output = process_intcode(puzzle_input, [5])
    print(program_output[-1])

#Task 2 Part 1
if int(args[1]) == 2: 
    processed_input, dump = process_intcode(puzzle_input, [])
    print('Part 1:', processed_input[0])

    #Part 2
    found = 0
    i = 0
    j = 0
    while found != 1 and j < 100:

        puzzle_input[1] = i
        puzzle_input[2] = j

        output = process_intcode(puzzle_input, [])

        if output[0] == 19690720:
            found = 1
            print('Part 2:', 100*i+j)

        i = i + 1
        if i > 99:
            i = 0
            j = j + 1

if int(args[1]) == 7:
    phases_perms = permutations([0, 1, 2, 3, 4])
    max_value = 0
    for i in range(0,2):
        print(i)
        program_output = [0]
        for phases in phases_perms:
            if i == 0:
                program_output = [0]
            dump, program_output = process_intcode(puzzle_input, [phases[0], program_output[-1]])
            dump, program_output = process_intcode(puzzle_input, [phases[1], program_output[-1]])
            dump, program_output = process_intcode(puzzle_input, [phases[2], program_output[-1]])
            dump, program_output = process_intcode(puzzle_input, [phases[3], program_output[-1]])
            dump, program_output = process_intcode(puzzle_input, [phases[4], program_output[-1]])
            if program_output[-1] > max_value:
                max_value = program_output[-1]
        phases_perms = permutations([5, 6, 7, 8, 9])
        print('max:', max_value)
        max_value = 0