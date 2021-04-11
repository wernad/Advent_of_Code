import intcode_computer as ic

puzzle_input = ic.load_input('17')

robot = ic.IntcodeComputer(puzzle_input)
robot.process_intcode()


area = dict()
x, y = 0, 0
x_temp = 0
for i in robot.output:
    if i == 35:
        area[(x, y)] = ('#')
        x += 1
    elif i == 10:
        y += 1
        x = 0

print(x, y)
