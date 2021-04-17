from collections import defaultdict, deque

with open('puzzle_input/input20.txt') as file:
    puzzle_input = [list(x.strip('\n')) for x in file.readlines()]

def find_portals(maze):
    def seek_function(coord, findPosition):
        global directions
        x1 = coord[0]
        y1 = coord[1]
        for x2, y2 in directions:
            x = x1 + x2
            y = y1 + y2
            if (x, y) in maze:
                if maze[(x, y)].isalpha() and not findPosition:
                    return (x, y), maze[(x, y)]
                if maze[(x, y)] == '.' and findPosition:
                    return (x, y)

    portals = defaultdict(set)
    start, end = None, None

    for k, v in maze.items():
        if v.isalpha() and k not in portals:
            portal_exit = seek_function(k, True)
            portal_other_half, portal_other_letter = seek_function(k, False)
            if not portal_exit:
                portal_exit = seek_function(portal_other_half, True)
            if v == 'A':
                start = portal_exit
            elif v == 'Z':
                end = portal_exit
            else:                
                portals[''.join(sorted(v + portal_other_letter))].add(portal_exit)
            
        
    return start, end, portals

def bfs(start, end):
    global portal_gates, maze
    
    visited = set(start)
    queue = deque([start])
    solution = dict()
    count = 0
    while queue:
        new_queue = deque()
        for position in queue:
            x = position[0]
            y = position[1]
            
            if position in portal_gates:
                new_queue.append(portal_gates[position])
                solution[portal_gates[position]] = position
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

maze = dict()

x, y = 0, 0
for line in puzzle_input:
    for i in line:
        if i.isalpha() or i == '.':
            maze[(x,y)] = i
        x += 1
    y += 1
    x = 0

directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

start_pos, end_pos, portals = find_portals(maze)     
portal_gates = {list(v)[0]: list(v)[1]  for _, v in portals.items()}

print(bfs(start_pos, end_pos))