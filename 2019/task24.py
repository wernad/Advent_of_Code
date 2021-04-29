with open('puzzle_input/input24.txt') as file:
    puzzle_input = [pos for line in file.readlines() for pos in list(line.strip('\n'))]

def add_tuples(a,b):
    return tuple([i + j for i, j in zip(a, b)])

def find_layout(initial_layout):
    global directions
    current_layout = initial_layout
    layouts = set()
    layouts.add(tuple(initial_layout))

    while True:
        new_layout = []
        for y in range(5):
            for x in range(5):
                neighbourhood = 0
                for i in directions:
                    if add_tuples(i, (x,y)) in current_layout:
                        neighbourhood += 1
                if ((x,y) in current_layout and neighbourhood == 1) or ((x,y) not in current_layout and neighbourhood in {1,2}):
                    new_layout.append((x,y))

        new_layout = tuple(new_layout)
        if new_layout in layouts:
            return new_layout

        layouts.add(new_layout)
        current_layout = new_layout


directions = [(1,0), (-1,0), (0,1), (0,-1)]

initial_layout = []
for y in range(5):
    for x in range(5):
        if puzzle_input.pop(0) == '#':
            initial_layout.append((x,y))

first_duplicate = find_layout(initial_layout)

powers_of_two = []
for y in range(5):
    for x in range(5):
        if (x,y) in first_duplicate:
            powers_of_two.append(2**(x+y*5))

print('Part 1:', sum(powers_of_two))