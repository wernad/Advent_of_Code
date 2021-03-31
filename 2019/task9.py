import intcode_computer as ic

puzzle_input = ic.load_input('9')

computer = ic.IntcodeComputer(puzzle_input)

computer.input = [1]
computer.process_intcode()
print('Part 1:', computer.output[-1])

computer.restart()
computer.input = [2]
computer.process_intcode()
print('Part 2:', computer.output[-1])