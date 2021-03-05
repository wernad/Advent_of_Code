def load_input(task_number):
    with open('puzzle_input/input' + task_number +'.txt') as file:
        puzzle_input = file.read()
        puzzle_input = puzzle_input.split(',')
        puzzle_input = [int(i) for i in puzzle_input]
    return puzzle_input

class IntcodeComputer:
    def __init__(self, puzzle_input, feedback):
        self.puzzle_input = puzzle_input.copy()
        self.puzzle_input_copy = puzzle_input.copy()
        self.opcode_position = 0
        self.relative_base = 0
        self.feedback = feedback
        self.input = []
        self.output = []

    def restart(self, puzzle_input = None):
        self.puzzle_input = self.puzzle_input_copy.copy() if puzzle_input is None else puzzle_input
        self.opcode_position = 0
        self.input = []
        return self

    def set_puzzle_input(self, puzzle_input):
        self.puzzle_input = puzzle_input.copy()

    def set_opcode_position(self, pos):
        self.opcode_position = pos

    def set_input(self, *program_input):
        self.input = []
        for x in program_input:
            self.input.append(x)
    
    def get_output(self):
        return self.output
    
    def get_puzzle_input(self):
        return self.puzzle_input

    def process_intcode(self):
        def __get_param(param_mode, value, add_only = False):
            if param_mode == 2:
                if len(self.puzzle_input) <= (value + self.relative_base):
                    self.puzzle_input.extend([0] * (value + self.relative_base - len(self.puzzle_input) + 1))
                return (value + self.relative_base) if add_only else self.puzzle_input[value + self.relative_base] 

            if len(self.puzzle_input) <= value and add_only:
                self.puzzle_input.extend([0] * (value - len(self.puzzle_input) + 1))
            if param_mode == 0:
                return value if add_only else self.puzzle_input[value] 

            return value

        self.output = []
        i = self.opcode_position
        while True:
            opcode = str(self.puzzle_input[i]).zfill(5)
            param_modes = [int(x) for x in opcode[:-2]]
            opcode = int(opcode[-2:])
            if opcode == 99:
                if self.feedback:
                    output = None
                break
            elif opcode in {3, 4, 9}:
                if opcode == 3: #input
                    param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1], True)                 
                    self.puzzle_input[param_1] = self.input.pop(0) if len(self.input) > 1 else self.input[0]
                elif opcode == 4: #output
                    param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                    self.output.append(param_1)
                    if self.feedback:
                        i += 2
                        self.opcode_position = i
                        break
                elif opcode == 9: #change relative base
                    param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                    self.relative_base += param_1
                i += 2
            elif opcode in {5, 6}:
                param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                param_2 = __get_param(param_modes[-2], self.puzzle_input[i+2])
                if opcode == 5:# jump if not equal to 0
                    i = param_2 if param_1 != 0 else i+3
                    continue
                elif opcode == 6: # jump if equal to 0
                    i = param_2 if param_1 == 0 else i+3
                    continue
            elif opcode in {1, 2, 7, 8}:
                param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                param_2 = __get_param(param_modes[-2], self.puzzle_input[i+2])
                param_3 = __get_param(param_modes[-3], self.puzzle_input[i+3], True)
                if opcode == 1: # a + b
                    self.puzzle_input[param_3] = param_1 + param_2
                elif opcode == 2: # a * b
                    self.puzzle_input[param_3] = param_1 * param_2
                elif opcode == 7: # 1 if a < b else 0
                    self.puzzle_input[param_3] = 1 if param_1 < param_2 else 0
                elif opcode == 8: # 1 if a == b else 0
                    self.puzzle_input[param_3] = 1 if param_1 == param_2 else 0
                i += 4
        