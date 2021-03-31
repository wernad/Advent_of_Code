import intcode_computer as ic

puzzle_input = ic.load_input('2')
computer = ic.IntcodeComputer(puzzle_input.copy())

#Part 1
computer.process_intcode()
print('Part 1:', computer.puzzle_input[0])
#Part 2
found = 0
i = 0
j = 0
while j < 100:
    puzzle_input[1] = i
    puzzle_input[2] = j

    computer.restart(puzzle_input.copy())
    computer.process_intcode()
    if computer.puzzle_input[0] == 19690720:
        break

    i = i + 1
    if i > 99:
        i = 0
        j = j + 1

print('Part 2:', 100*i+j)