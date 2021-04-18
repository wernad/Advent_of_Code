from collections import defaultdict, deque

with open('puzzle_input/input20.txt') as file:
    puzzle_input = [list(x.strip('\n')) for x in file.readlines()]

def bfs(start, end, maze):
    global portals
    
    visited = set(start)
    queue = deque([start])
    solution = dict()
    
    while queue:
        new_queue = deque()
        for position in queue:
            x = position[0]
            y = position[1]
            
            if position in portals and portals[position] not in visited:
                new_queue.append(portals[position])
                solution[portals[position]] = position
                visited.add(position)
                continue

            new_pos = (x + 1, y)
            if new_pos in maze and new_pos not in visited:
                new_queue.append(new_pos)
                solution[new_pos] = position
                
            new_pos = (x - 1, y)
            if new_pos in maze and new_pos not in visited:
                new_queue.append(new_pos)
                solution[new_pos] = position
                
            new_pos = (x, y + 1)
            if new_pos in maze and new_pos not in visited:
                new_queue.append(new_pos)
                solution[new_pos] = position
                
            new_pos = (x, y - 1)
            if new_pos in maze and new_pos not in visited:
                new_queue.append(new_pos)
                solution[new_pos] = position
            
            visited.add(position)

        queue = new_queue
    count = 0
    current_coord = end
    while current_coord != start:
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

print(bfs(start, end, maze))