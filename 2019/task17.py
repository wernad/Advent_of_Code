import re
import intcode_computer as ic

puzzle_input = ic.load_input('17')

class vacuumRobot(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(vacuumRobot, self).__init__(*args, **kwargs)
        self.position = None
        self.direction = 90
        self.scaffolds = []
        self.path = ''

    def draw_area(self):
        area = ''
        for i in robot.output:
            if i == 46:
                area += '.'
            elif i == 35:
                area += '#'
            elif i == 10:
                area += '\n'
            else:
                area += chr(i)
        print(area)

    def find_scaffolds(self):
        x, y = 0, 0
        for i in robot.output:
            if i == 46:
                x += 1
            elif i == 35:
                self.scaffolds.append((x, y))
                x += 1
            elif i == 10:
                y += 1
                x = 0
            elif i != 10:
                self.position = (x, y)
                x += 1

    def generate_path(self):
        direction_dict = {
            0 : (1, 0),
            90 : (0, -1),
            180 : (-1, 0),
            270 : (0, 1)
        }

        last_pos = self.position
        distance = 0
        buffer = []
        while True:
            new_pos = tuple(sum(x) for x in zip(direction_dict[self.direction], self.position))
            if new_pos in self.scaffolds:
                last_pos = self.position
                self.position = new_pos
                distance += 1
                continue
            
            if self.path:
                self.path += str(distance)
                distance = 0

            for turn in [('L', 90), ('R', -90)]:
                new_pos = tuple(sum(x) for x in zip(direction_dict[(self.direction + turn[1]) % 360], self.position))
                if new_pos in self.scaffolds and new_pos != last_pos:
                    self.path += turn[0]
                    self.direction += turn[1]
                    self.direction %= 360
                    break
            else:
                break
        
    def path2functions(self):
        path_string = ''.join(str(x) for x in self.path)
        last_pattern = ''
        current_pattern = ''
        functions = []
        while path_string:
            for i in range(2,len(path_string), 2):               
                if len(re.findall(path_string[0:i], path_string)) > 1:
                    current_pattern = path_string[0:i]
                else:
                    path_string = path_string.replace(current_pattern, '')
                    if path_string in current_pattern:
                        current_pattern = current_pattern.replace(path_string, '')
                        functions.append(path_string)
                        path_string = ''
                    functions.append(current_pattern)
                    current_pattern = ''                    
                    break

        return functions

    def create_routine(self, functions):
        path_string = ''.join(str(x) for x in self.path)
        
        for x,y in zip(functions, ['A','B','C']):
            path_string = path_string.replace(x, y)
        
        main_routine = ','.join(x for x in path_string)
        
        return main_routine

#Splits steps that are higher than 9 into multiple single digit ones, e.g., L10 -> L9L1
def simplify_functions(functions):
    max_ASCII_num = 9
    for k,v in enumerate(functions):
        print(v)
        multi_digit = set(re.findall(r'\d\d+', v))
        for x in multi_digit:
            new_digit = int(x)
            replacement = ''
            while new_digit > max_ASCII_num:
                new_digit = new_digit - max_ASCII_num
                replacement += str(max_ASCII_num)
            replacement += str(new_digit)
            functions[k] = v.replace(x, replacement)

    return functions    

robot = vacuumRobot(puzzle_input)
robot.process_intcode()

robot.find_scaffolds()

intersections = []
for pos in robot.scaffolds:
    x = pos[0]
    y = pos[1]
    if all(new_pos in robot.scaffolds for new_pos in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]):
        intersections.append(pos)

robot.generate_path()
functions = robot.path2functions()
main_routine = robot.create_routine(functions)
functions = [','.join(x) for x in simplify_functions(functions)]

puzzle_input[0] = 2
robot.puzzle_input = puzzle_input

robot.input = robot.list2ASCII(main_routine)
for x in functions:
    robot.input.extend(robot.list2ASCII(x))
robot.input.extend([ord('n'), 10])
robot.process_intcode()

print('Part 1:', sum([x[0] * x[1] for x in intersections]))
print('Part 2:', robot.output[-1])