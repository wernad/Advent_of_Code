import intcode_computer as ic

puzzle_input = ic.load_input('5')

computer = ic.IntcodeComputer(puzzle_input.copy(), False)

computer.set_input([1])
computer.process_intcode()
print('Part 1:', computer.get_output()[-1])

computer.restart()
computer.set_input([5])
computer.process_intcode()
print('Part 2:', computer.get_output()[-1])