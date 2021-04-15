from itertools import count
import intcode_computer as ic

puzzle_input = ic.load_input('19')

drone = ic.IntcodeComputer(puzzle_input)

def count_beam_size(x_max, y_max):
    area = ''
    x_min = 0
    for y in range(y_max):
        for x in range(x_min, x_max):       
            drone.input = [x, y]
            drone.process_intcode()
            if drone.output[-1] == 0:
                if area[-1] == '#':
                    drone.restart()
                    break
                area += '.'
            else:
                if area:
                    if area[-1] != '#':
                        x_min = x
                area += '#'
            drone.restart()
        area += '\n'    
    return area.count('#')

def find_closest_point(square_side):
    last = ''
    x_min = 0
    x_max = 3
    for y in count(start=0):
        print(y, x_min, x_max)
        for x in range(x_min, x_max):   
            drone.input = [x, y]
            drone.process_intcode()
            output = drone.output[-1]
            drone.restart()
            if output == 0:
                if last == '#':
                    x_max = x + 3
                    break
                last = '.'
            else:
                if last != '#':
                    drone.input = [x + square_side - 1, y - square_side + 1]
                    drone.process_intcode()
                    if drone.output[-1] == 1:
                        return x * 10000 + (y - square_side + 1)
                    drone.restart()
                    x_min = x
                last = '#'
        last = '\n'   

x_max, y_max = 50, 50
square_side = 100

print('Part 1:', count_beam_size(x_max, y_max))
#drone.restart()
print('Part 2:', find_closest_point(square_side))