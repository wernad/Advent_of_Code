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

    def get_position(self):
        return self.position

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
                if robot.get_panels().get(robot.get_position(), '.') == '.': 
                    robot.set_input(0)
                else:
                    robot.set_input(1)
                robot.process_intcode()
                if robot.get_output() == []:
                    break
                output.append(robot.get_output()[-1])
            if robot.get_output() == []:
                break
            self.panels[self.position] = '.' if output[0] == 0 else '#'
            robot.move(output[1])        

robot = paintingRobot(puzzle_input, True)

robot.paint()

print('Part 1:', len(robot.get_panels()))

panels = [k for k in robot.get_panels()]

grid_bottom_left = (min(panels, key=lambda x: x[0])[0], min(panels, key=lambda x: x[1])[1])
grid_top_right = (max(panels, key=lambda x: x[0])[0], max(panels, key=lambda x: x[1])[1])

grid_width = abs(grid_bottom_left[0] - grid_top_right[0])
grid_height = abs(grid_bottom_left[1] - grid_top_right[1])

robot.restart()
robot.add_panel('#')
robot.paint()

identifier = np.chararray(shape=(grid_width, grid_height), unicode=True)
identifier[:] = '..'
img = Image.new('RGB', (grid_width,grid_height),"black")
for key in robot.get_panels():
    if robot.get_panels()[key] == '#':
        img.putpixel((key[0] + abs(grid_bottom_left[0]), key[1] + abs(grid_bottom_left[1])), (0,0,255,255))
        #identifier[key[0] + abs(grid_bottom_left[0])][key[1] + abs(grid_bottom_left[1])] = '#'

img = img.transpose(Image.FLIP_TOP_BOTTOM)

img.show()
