import intcode_computer as ic

from itertools import permutations 

puzzle_input = ic.load_input('7')

def max_signal(puzzle_input):
    phases = permutations([0, 1, 2, 3, 4])
    amp = ic.IntcodeComputer(puzzle_input.copy(), False)
    values = []
    for phase in phases:    
        last_output = 0
        for i in range(5):
            amp.set_input(phase[i], last_output)
            amp.process_intcode()
            last_output = amp.get_output()[-1]
            amp.restart()
        values.append(last_output)
    return max(values)

def max_signal_feedback(puzzle_input):
    phases = permutations([5, 6, 7, 8, 9])
    amps = [ic.IntcodeComputer(puzzle_input.copy(), True) for i in range(5)]
    values = []
    for phase in phases:
        amps = [amp.restart() for amp in amps]
        last_output = 0
        finished = False
        for i in range(5):
            amps[i].set_input(phase[i], last_output)
            amps[i].process_intcode()
            last_output = amps[i].get_output()
        while not finished:
            for i in range(5):
                amps[i].set_input(last_output)
                amps[i].process_intcode()
                if amps[i].get_output():
                    last_output = amps[i].get_output()
                else:
                    finished = True
                    break
        values.append(last_output)
    return max(values)
            
print('Part 1:', max_signal(puzzle_input))
print('Part 2:', max_signal_feedback(puzzle_input))