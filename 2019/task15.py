import intcode_computer as ic
from collections import defaultdict, deque

puzzle_input = ic.load_input('15')

class repairDroid(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(repairDroid, self).__init__(*args, **kwargs)
        self.available_moves = defaultdict((lambda: [1,2,3,4]), {(0, 0): [1,2,3,4]})
        self.position = (0,0)
        self.oxygen_system = None
        self.area = [(0,0)]

    def opposite_direction(self, direction):
        direction_dict = {
            1: 2, 
            2: 1, 
            3: 4, 
            4: 3
        }
        return direction_dict[direction]

    def calc_new_pos(self, direction):
        new_position = None
        if direction == 1:
            new_position = (self.position[0], self.position[1] + 1)
        elif direction == 2:
            new_position = (self.position[0], self.position[1] - 1)
        elif direction == 3:
            new_position = (self.position[0] - 1, self.position[1])
        elif direction == 4:
            new_position = (self.position[0] + 1, self.position[1])                    
        return new_position

    def dfs(self):
        backtrack = deque()
        visited = set(self.position)
        path_length = 0
        while len(self.available_moves[(0,0)]) > 0:
            
            if len(self.available_moves[self.position]) == 0:
                dir_back = backtrack.pop()
                new_pos = self.calc_new_pos(dir_back)
                self.position = new_pos
                self.input = [dir_back]
                self.process_intcode()
                continue

            direction = self.available_moves[self.position].pop(0)
            new_pos = self.calc_new_pos(direction)
            if new_pos in visited:
                continue

            self.input = [direction]
            self.process_intcode()
            
            if self.output[-1] == 0:
                continue

            self.position = new_pos
            backtrack.append(self.opposite_direction(direction))

            if self.output[-1] == 2:
                path_length = len(backtrack)
                self.oxygen_system = self.position

            visited.add(self.position)
            self.area.append(self.position)
        return path_length

    def bfs(self):
        visited = set(self.oxygen_system)
        queue = deque([self.oxygen_system])
        time_to_fill = 0
        while queue:
            new_queue = deque()
            for position in queue:
                x = position[0]
                y = position[1]
                if (x + 1, y) in self.area and (x + 1, y) not in visited:
                    new_queue.append((x + 1, y))
                if (x - 1, y) in self.area and (x - 1, y) not in visited:
                    new_queue.append((x - 1, y))
                if (x, y + 1) in self.area and (x, y + 1) not in visited:
                    new_queue.append((x, y + 1))
                if (x, y - 1) in self.area and (x, y - 1) not in visited:
                    new_queue.append((x, y - 1))
                visited.add(position)
            queue = new_queue
            if queue:
                time_to_fill += 1
        return time_to_fill
            
droid = repairDroid(puzzle_input, True)
print('Part 1:', droid.dfs())
print('Part 2:', droid.bfs())