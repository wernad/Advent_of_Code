import intcode_computer as ic

puzzle_input = ic.load_input('21')

class springDroid(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(springDroid, self).__init__(*args, **kwargs)
        self.scaffolds = dict()
        self.path = ''

def list2ASCII(input_list):
    new_list = [ord(x) for x in input_list]
    new_list.append(10)
    return new_list
    
def ASCII2list(input_list):
    return [chr(x) for x in input_list]

droid = springDroid(puzzle_input)

intructions = '''NOT B J
NOT C T
OR T J
NOT A T
OR T J
AND D J
OR T J
WALK'''

droid.input = list2ASCII(intructions)

droid.process_intcode()
print('Part 1:', droid.output[-1])
#''.join(ASCII2list(droid.output))