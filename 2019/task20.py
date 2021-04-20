from collections import defaultdict, deque
from copy import deepcopy 

with open('puzzle_input/input20.txt') as file:
    puzzle_input = [list(x.strip('\n')) for x in file.readlines()]

def bfs(start, end, maze):
    global portals
    
    visited = set(start)
    queue = deque([start])
    solution = {start: start}
    
    while queue:
        new_queue = deque()
        for position in queue:
            x = position[0]
            y = position[1]

            for new_pos in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if new_pos in maze and new_pos not in visited:
                    new_queue.append(new_pos)
                    solution[new_pos] = position

            if position in portals and portals[position] not in visited:
                new_queue.append(portals[position])
                solution[portals[position]] = position
        
            visited.add(position)

        queue = new_queue
    count = 0
    current_coord = end
    while current_coord != start:
        current_coord = solution[current_coord]
        count += 1

    return count

def bfs_layered(start, end, maze):
    global portals
    
    outer_x = set([max([x[0] for x in portals]), min([x[0] for x in portals])])
    outer_y = set([max([x[1] for x in portals]), min([x[1] for x in portals])])
    visited = set([(start, 0)])
    queue = deque([(start, 0)])
    solution = {(start, 0): (start, 0)}
    found = False
    while any(len(x) > 0 for x in queue) and not found:
        new_queue = deque()
        for position, layer in queue:
            #print(layer)
            x = position[0]
            y = position[1]

            for new_pos in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if new_pos in maze and (new_pos, layer) not in visited:
                    new_queue.append((new_pos, layer))
                    solution[(new_pos, layer)] = (position, layer)
                    if (new_pos, layer) == (end, 0):
                        found = True

            if position in portals and (position, layer) not in visited:
                new_layer = layer
                if x in outer_x or y in outer_y:
                    if layer == 0:
                        continue
                    new_layer -= 1
                elif x not in outer_x or y not in outer_y:
                    if layer + 1 >= len(portals)//2:
                        continue
                    new_layer += 1
                
                solution[(portals[position], new_layer)] = (position, layer)                    
                new_queue.append((portals[position], new_layer))
                visited.add((portals[position], new_layer))
                
            visited.add((position, layer))
        queue = new_queue
    
    count = 0
    current_coord = (end, 0)
    while current_coord != (start, 0):
        current_coord = solution[current_coord]
        count += 1

    return count

def add_tuples(a,b):
    return tuple([i + j for i, j in zip(a, b)])

def check_neighbours(a,b):
    global directions
    return True if tuple([abs(i - j) for i, j in zip(a, b)]) in directions else False

def find_open_passage(pos1, pos2):

    global directions
    for d in directions:
        new_pos = add_tuples(pos1, d)
        if new_pos in maze:
            return new_pos 

        new_pos = add_tuples(pos2, d)
        if new_pos in maze:
            return new_pos 

def construct_portals(maze, portal_letters):
    start, end = None, None
    portals = defaultdict(list)

    while portal_letters:
        a = portal_letters.popitem()
        b = None
        for new_b in portal_letters.items():
            if check_neighbours(a[0],new_b[0]):
                b = new_b
                break
        del portal_letters[b[0]]
        portal_name = ''.join(sorted(a[1]+b[1]))
        portal_entrance = find_open_passage(a[0],b[0])
        if portal_name == 'AA':
            start = portal_entrance
            continue
        elif portal_name == 'ZZ':
            end = portal_entrance
            continue
        portals[portal_name].append(portal_entrance)

    portals = {k: v for _, entrances in portals.items() for k,v in zip((entrances[0], entrances[1]), (entrances[1], entrances[0]))}
    return start, end, portals
       

maze = dict()
portal_letters = dict()

x, y = 0, 0
for line in puzzle_input:
    for i in line:
        if i.isalpha():
            portal_letters[(x,y)] = i
        elif i == '.':
            maze[(x,y)] = i
        x += 1
    y += 1
    x = 0

directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
start, end, portals = construct_portals(maze, portal_letters)

print('Part 1:', bfs(start, end, maze))
print('Part 2:', bfs_layered(start, end, maze))