import intcode_computer as ic

puzzle_input = ic.load_input('21')

class springDroid(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(springDroid, self).__init__(*args, **kwargs)
        self.scaffolds = dict()
        self.path = ''

droid = springDroid(puzzle_input)

walk_program = '''NOT C T
OR T J
NOT A T
OR T J
AND D J
WALK'''

run_program = '''NOT B J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN'''

droid.input = droid.list2ASCII(walk_program)
droid.process_intcode()
output1 = droid.output[-1]

droid.restart()
droid.input = droid.list2ASCII(run_program)
droid.process_intcode()
output2 = droid.output[-1]

print('Part 1:', output1)
print('Part 2:', output2)
