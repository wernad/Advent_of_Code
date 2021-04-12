import re
import intcode_computer as ic

puzzle_input = ic.load_input('17')

class vacuumRobot(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(vacuumRobot, self).__init__(*args, **kwargs)
        self.position = None
        self.direction = 90
        self.scaffolds = dict()
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
                self.scaffolds[(x, y)] = ('#')
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

            new_pos = tuple(sum(x) for x in zip(direction_dict[(self.direction + 90) % 360], self.position))
            if new_pos in self.scaffolds and new_pos != last_pos:
                self.path += 'L'
                self.direction += 90
                self.direction %= 360
                continue

            new_pos = tuple(sum(x) for x in zip(direction_dict[(self.direction - 90) % 360], self.position))
            if new_pos in self.scaffolds and new_pos != last_pos:
                self.path += 'R'
                self.direction -= 90
                self.direction %= 360
                continue
            break
        
    def find_routine(self):
        path_string = ''.join(str(x) for x in self.path)
        main_routine = path_string
        last_pattern = ''
        current_pattern = ''
        functions = []
        for x in range(0,3):
            if x == 2:
                functions.append(path_string)
                break
            for i in range(2,len(path_string), 2):
                if len(current_pattern) == 0:
                    current_pattern = path_string[0:i]
                    last_pattern = current_pattern
                    continue

                current_pattern = path_string[0:i]
                if len(re.findall(current_pattern, path_string)) > 1:
                    last_pattern = current_pattern
                else:
                    functions.append(last_pattern)
                    path_string = path_string.replace(last_pattern, '')
                    last_pattern = ''
                    current_pattern = ''
                    break
        
        #Remove duplicates between patterns.
        functions.sort(key=lambda x: len(x))
        for i in range(0, len(functions)-1):
            for j in range(i+1, len(functions)):
                if functions[i] in functions[j]:
                    functions[j] = functions[j].replace(functions[i], '')
        
        for x,y in zip(functions, ['A','B','C']):
            main_routine = main_routine.replace(x, y)

        main_routine = ','.join(x for x in main_routine)

        max_ASCII_num = 9
        for k,v in enumerate(functions):
            multi_digit = set(re.findall(r'\d\d', v))
            for x in multi_digit:
                new_digit = int(x)
                replacement = ''
                while new_digit > max_ASCII_num:
                    new_digit = new_digit - max_ASCII_num
                    replacement += str(max_ASCII_num)
                replacement += str(new_digit)
                functions[k] = v.replace(x, replacement)

        functions = [','.join(x) for x in functions]

        return main_routine, functions

def list2ASCII(input_list):
    new_list = [ord(x) for x in input_list]
    new_list.append(10)
    return new_list

def ASCII2list(input_list):
    return [chr(x) for x in input_list]

robot = vacuumRobot(puzzle_input)
robot.process_intcode()
#robot.draw_area()
robot.find_scaffolds()

intersections = []
for i in robot.scaffolds:
    x = i[0]
    y = i[1]
    if all(j in robot.scaffolds for j in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]):
        intersections.append(i)

robot.generate_path()
main_routine, functions = robot.find_routine()

puzzle_input[0] = 2
robot.puzzle_input = puzzle_input

robot.input = list2ASCII(main_routine)
for x in functions:
    robot.input.extend(list2ASCII(x))
robot.input.extend([ord('n'), 10])

robot.process_intcode()

print('Part 1:', sum([x[0] * x[1] for x in intersections]))
print('Part 2:', robot.output[-1])