from itertools import tee
import more_itertools

with open('puzzle_input/input3.txt') as file:
    puzzle_input = file.read()
    wire1_steps, wire2_steps = puzzle_input.split('\n')
    wire1_steps = [(x[0], int(x[1:])) for x in wire1_steps.split(',')]
    wire2_steps = [(x[0], int(x[1:])) for x in wire2_steps.split(',')]

# Returns list of endpoints of line segments the wire consists of.
def draw_wire(wire_steps):
    coords = [(0, 0, 0)] #[(x,y,distance)]
    for step in wire_steps:
        x, y, distance = coords[-1][0], coords[-1][1], coords[-1][2]
        if step[0] == 'L':
            x -= step[1]
        elif step[0] == 'R':
            x += step[1]
        elif step[0] == 'U':
            y += step[1]
        elif step[0] == 'D':
            y -= step[1]
        distance += step[1]
        coords.append((x, y, distance))
    return coords

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

# 0 -> horizontal
# 1 -> vertical
def get_line_type(a,b):
    if a[0] == b[0]:
        return 1
    return 0

#Compares all lines among both wires and finds intersections.
def find_intersections(wire1, wire2):
    intersections = []
    distances = []
    
    for a1, a2 in pairwise(wire1):
        a1_coords = a1[0], a1[1]
        a2_coords = a2[0], a2[1]
        
        wire1_type = get_line_type(a1_coords, a2_coords)
        
        for b1, b2 in pairwise(wire2):
            b1_coords = b1[0], b1[1]
            b2_coords = b2[0], b2[1]
            wire2_type = get_line_type(b1_coords, b2_coords)

            if wire1_type == wire2_type: #paralel lines
                continue

            if wire1_type == 1 and ((b1_coords[0] < a1_coords[0] < b2_coords[0]) or (b2_coords[0] < a1_coords[0] < b1_coords[0])) and ((a1_coords[1] < b1_coords[1] < a2_coords[1]) or (a2_coords[1] < b1_coords[1] < a1_coords[1])):
                intersections.append((a1_coords[0], b1_coords[1]))
                distances.append(a1[2] + b1[2] + abs(a1_coords[0] - b1_coords[0]) + abs(a1_coords[1] - b1_coords[1])) #part 2
            elif ((a1_coords[0] < b1_coords[0] < a2_coords[0]) or (a2_coords[0] < b1_coords[0] < a1_coords[0])) and ((b1_coords[1] < a1_coords[1] < b2_coords[1]) or (b2_coords[1] < a1_coords[1] < b1_coords[1])):
                intersections.append((b1_coords[0], a1_coords[1]))
                distances.append(a1[2] + b1[2] + abs(a1_coords[0] - b1_coords[0]) + abs(a1_coords[1] - b1_coords[1])) #part 2

    return intersections, distances

#Calculates returns minimum manhattan_distance from all intersections.
def find_shortest_md(intersections):
    distances = []

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    for x,y in intersections:
        distances.append(manhattan_distance((0,0), (x,y)))
    return min(distances)


wire1 = draw_wire(wire1_steps)
wire2 = draw_wire(wire2_steps)

intersections, distances = find_intersections(wire1, wire2)
print('Part 1:', find_shortest_md(intersections))
print('Part 2:', min(distances))