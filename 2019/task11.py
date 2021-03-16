import intcode_computer as ic
import numpy as np

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
        if turn == 0:
            self.direction -= 90
        else:
            self.direction += 90 
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
            if output[0] == 0:
                robot.add_panel('.')
            else:
                robot.add_panel('#')
            robot.move(output[1])        

robot = paintingRobot(puzzle_input, True)
robot.paint()

print('Part 1:', len(robot.get_panels()))

panels = []
for k in robot.get_panels():
    panels.append(k)

grid_bottom_left = (min(panels, key=lambda x: x[0])[0], min(panels, key=lambda x: x[1])[1])
grid_top_right = (max(panels, key=lambda x: x[0])[0], max(panels, key=lambda x: x[1])[1])

grid_width = abs(grid_bottom_left[0] - grid_top_right[0])
grid_height = abs(grid_bottom_left[1] - grid_top_right[1])
robot.restart()
robot.add_panel('#')
robot.paint()

identifier = np.chararray(shape=(grid_height, grid_width))
for key in robot.get_panels():
    identifier[key[0]][key[1]] = robot.get_panels()[key]
np.savetxt('identifier.csv', identifier, fmt='%s')
