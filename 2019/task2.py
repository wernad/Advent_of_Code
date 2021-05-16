import intcode_computer as ic

def find_input(puzzle_input, output):
    for j in range(100):
        for i in range(100):
            puzzle_input[1] = i
            puzzle_input[2] = j

            computer = ic.IntcodeComputer(puzzle_input)
            computer.process_intcode()
            if computer.puzzle_input[0] == 19690720:
                return i*100+j

puzzle_input = ic.load_input('2')
computer = ic.IntcodeComputer(puzzle_input)

computer.process_intcode()

OUTPUT = 19690720

print('Part 1:', computer.puzzle_input[0])
print('Part 2:', find_input(puzzle_input, OUTPUT))