import intcode_computer as ic

from itertools import permutations 

puzzle_input = ic.load_input('7')

def max_signal(puzzle_input):
    phases = permutations([0, 1, 2, 3, 4])
    amp = ic.IntcodeComputer(puzzle_input)
    values = []
    for phase in phases:    
        last_output = 0
        for i in range(5):
            amp.input = [phase[i], last_output]
            amp.process_intcode()
            last_output = amp.output[-1]
            amp.restart()
        values.append(last_output)
    return max(values)

def max_signal_feedback(puzzle_input):
    phases = permutations([5, 6, 7, 8, 9])
    amps = [ic.IntcodeComputer(puzzle_input, True) for i in range(5)]
    values = []
    for phase in phases:
        amps = [amp.restart() for amp in amps]
        last_output = 0
        for i in range(5):
            amps[i].input = [phase[i], last_output]
            amps[i].process_intcode()
            last_output = amps[i].output[-1]
        while all(x.turned_on for x in amps):
            for i in range(5):
                amps[i].input = [last_output]
                amps[i].process_intcode()
                last_output = amps[i].output[-1]

        values.append(last_output)
    return max(values)
            
print('Part 1:', max_signal(puzzle_input))
print('Part 2:', max_signal_feedback(puzzle_input))