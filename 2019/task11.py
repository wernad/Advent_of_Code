import intcode_computer as ic
import numpy as np
from PIL import Image
from collections import defaultdict

puzzle_input = ic.load_input('11')

class paintingRobot(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(paintingRobot, self).__init__(*args, **kwargs)
        self.panels = defaultdict(lambda: '.')
        self.position = (0,0)
        self.direction = 90

    def restart(self, *args, **kwargs):
        super(paintingRobot, self).restart(*args, **kwargs)
        self.panels = defaultdict(lambda: '.')
        self.position = (0,0)
        self.direction = 90

    def add_panel(self, color):
        self.panels[self.position] = color

    def move(self, turn):
        movements_dict = {
            0: lambda x: (x[0] + 1, x[1]),
            90: lambda x: (x[0], x[1] + 1),
            180: lambda x: (x[0] - 1, x[1]),
            270: lambda x: (x[0], x[1] - 1),
        }
        self.direction += 90 if turn == 0 else -90
        self.direction %= 360

        self.position = movements_dict[self.direction](self.position)
    
    def paint(self):
        while self.turned_on:
            output = []
            while len(output) < 2:
                if self.panels[self.position] == '.': 
                    self.input = [0]
                else:
                    self.input = [1]
                self.process_intcode()
                output.append(self.output[-1])
            self.panels[self.position] = '.' if output[0] == 0 else '#'
            self.move(output[1])        

robot = paintingRobot(puzzle_input, True)

robot.paint()
print('Part 1:', len(robot.panels))

robot = paintingRobot(puzzle_input, True)
robot.add_panel('#')
robot.paint()

identifier_panels = [x for x in robot.panels if robot.panels[x] == '#']

#Finds corners of identifier image
identifier_bottom_left = (min(identifier_panels, key=lambda x: x[0])[0], min(identifier_panels, key=lambda x: x[1])[1])
identifier_top_right = (max(identifier_panels, key=lambda x: x[0])[0], max(identifier_panels, key=lambda x: x[1])[1])

#Calculates dimensions
identifier_width = abs(identifier_bottom_left[0] - identifier_top_right[0]) + 1# + 1 to include last coordinate
identifier_height = abs(identifier_bottom_left[1] - identifier_top_right[1]) + 1

identifier = np.ndarray(shape=(identifier_width, identifier_height), dtype='U3')
identifier[:] = ' '

for coord in robot.panels:
    if robot.panels[coord] == '#':
        identifier[coord[0] - 1][coord[1] + abs(identifier_bottom_left[1])] = '#'
        
identifier = identifier[:-1, :]
identifier_string = '\n'.join(''.join(y for y in x) for x in np.rot90(identifier))

print('Part 2:', identifier_string, sep='\n')
