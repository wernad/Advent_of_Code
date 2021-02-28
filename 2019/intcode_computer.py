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
        def __get_param(param_mode, value):
            if param_mode == 0:
                return self.puzzle_input[value]
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
                return
            elif opcode in {3, 4}:
                if opcode == 3: #input
                    self.puzzle_input[self.puzzle_input[i+1]] = self.input.pop(0) if len(self.input) > 1 else self.input[0]
                elif opcode == 4: #output
                    param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                    self.output.append(param_1)
                    if self.feedback:
                        i += 2
                        self.opcode_position = i
                        return
                i += 2
            elif opcode in {1, 2, 5, 6, 7, 8}:
                param_1 = __get_param(param_modes[-1], self.puzzle_input[i+1])
                param_2 = __get_param(param_modes[-2], self.puzzle_input[i+2])
                if opcode == 1: # a + b
                    self.puzzle_input[self.puzzle_input[i+3]] = param_1 + param_2
                elif opcode == 2: # a * b
                    self.puzzle_input[self.puzzle_input[i+3]] = param_1 * param_2
                elif opcode == 5:# jump if not equal to 0
                    i = param_2 if param_1 != 0 else i+3
                    continue
                elif opcode == 6: # jump if equal to 0
                    i = param_2 if param_1 == 0 else i+3
                    continue
                elif opcode == 7: # 1 if a < b else 0
                    self.puzzle_input[self.puzzle_input[i+3]] = 1 if param_1 < param_2 else 0
                elif opcode == 8: # 1 if a == b else 0
                    self.puzzle_input[self.puzzle_input[i+3]] = 1 if param_1 == param_2 else 0
                i += 4
        