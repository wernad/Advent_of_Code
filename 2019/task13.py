import intcode_computer as ic
from collections import defaultdict

puzzle_input = ic.load_input('13')

arcade = ic.IntcodeComputer(puzzle_input.copy(), False)
arcade.process_intcode()
arcade_output = arcade.get_output()

count = 0
for i in range(0, len(arcade_output), 3):
    if arcade_output[i+2] == 2:
        count += 1

print(count)





        
    