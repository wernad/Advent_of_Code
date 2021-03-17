import intcode_computer as ic
import numpy as np
from PIL import Image

puzzle_input = ic.load_input('11')

class paintingRobot(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(paintingRobot, self).__init__(*args, **kwargs)
        self.panels = dict()
        self.position = (0,0)
        self.direction = 90

    def restart(self, *args, **kwargs):
        super(paintingRobot, self).restart(*args, **kwargs)
        self.panels = dict()
        self.position = (0,0)
        self.direction = 90

    def get_panels(self):
        return self.panels

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
        while True:
            output = []
            while len(output) < 2:
                if self.panels.get(self.position, '.') == '.': 
                    robot.set_input(0)
                else:
                    robot.set_input(1)
                robot.process_intcode()
                if self.output == []:
                    break
                output.append(self.output[-1])
            if self.output == []:
                break
            self.panels[self.position] = '.' if output[0] == 0 else '#'
            robot.move(output[1])        

robot = paintingRobot(puzzle_input, True)

robot.paint()
print('Part 1:', len(robot.get_panels()))

robot.restart()
robot.add_panel('#')
robot.paint()

identifier_panels = [x for x in robot.get_panels() if robot.get_panels()[x] == '#']

identifier_bottom_left = (min(identifier_panels, key=lambda x: x[0])[0], min(identifier_panels, key=lambda x: x[1])[1])
identifier_top_right = (max(identifier_panels, key=lambda x: x[0])[0], max(identifier_panels, key=lambda x: x[1])[1])

identifier_width = abs(identifier_bottom_left[0] - identifier_top_right[0]) + 1 # + 1 to include last coordinate
identifier_height = abs(identifier_bottom_left[1] - identifier_top_right[1]) + 1

identifier = np.chararray(shape=(identifier_width, identifier_height), unicode=True)
identifier[:] = '-'

for key in robot.get_panels():
    if robot.get_panels()[key] == '#':
        identifier[key[0] - 1][key[1] + abs(identifier_bottom_left[1])] = '#'
 
identifier_string = '\n'.join(''.join('%s' %y for y in x) for x in np.rot90(identifier))

print('Part 2:\n', identifier_string, sep='')
