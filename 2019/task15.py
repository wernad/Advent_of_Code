import intcode_computer as ic
from collections import defaultdict

puzzle_input = ic.load_input('15')

class repairDroid(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(repairDroid, self).__init__(*args, **kwargs)
        self.available_moves = defaultdict((lambda: [1,2,3,4]), {(0, 0): [1,2,3,4]})
        self.position = (0,0)
        self.oxygen_system = None
        self.area = dict()

    def add_coord(self, parent, child):
        self.area[parent].append(child)

    def restart(self, *args, **kwargs):
        super(repairDroid, self).restart(*args, **kwargs)
        self.available_moves = defaultdict(lambda: [1,2,3,4], {(0, 0): [1,2,3,4]})
        self.position = (0,0)
        self.backtrack = []

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
        backtrack = []
        solution = {self.position : self.position}
        visited = set(self.position)
        visited.add(self.position)
        path_length = float('inf')
        while len(self.available_moves[(0,0)]) > 0 or self.position != (0,0):
            
            if len(self.available_moves[self.position]) == 0:
                dir_back = backtrack.pop(-1)
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
        return path_length
            
            
droid = repairDroid(puzzle_input, True)
print('Part 1:', droid.dfs())