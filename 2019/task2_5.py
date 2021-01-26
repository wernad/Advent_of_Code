with open('input') as file:
    program_input = file.read()
    program_input = program_input.replace(',', ' ').split()
    program_input = [int(i) for i in program_input]

def process_intcode(program_input):
    i = 0
    j = 0
    while i <= len(program_input):
        opcode = str(program_input[i])
        param_modes = None
        if len(opcode) > 2:
            param_modes = opcode[:-2]
            opcode = opcode[-2:].lstrip('0')
        print('run:', j, 'opcode:', program_input[i], 'at [{}]'.format(i), 'param_modes:', param_modes)
        if opcode == '99':
            break
        elif opcode in {'1', '2', '5', '6', '7', '8'}:
            param_1, param_2 = None, None
            try:
                if param_modes[-1] == '0':
                    param_1 = program_input[program_input[i+1]]
                else:
                    param_1 = program_input[i+1]
            except (TypeError, IndexError):
                param_1 = program_input[program_input[i+1]]

            try:
                if param_modes[-2] == '0':
                    param_2 = program_input[program_input[i+2]]
                else:
                    param_2 = program_input[i+2]
            except (TypeError, IndexError):
                param_2 = program_input[program_input[i+2]]
            
            param_1, param_2 = int(param_1), int(param_2)

            print('param1:', param_1, 'param2:', param_2, 'store address: [{}]'.format(program_input[i+3]))
            if opcode == '1':
                program_input[program_input[i+3]] = param_1 + param_2
            elif opcode == '2':
                program_input[program_input[i+3]] = param_1 * param_2
            elif opcode == '5':
                i = param_2 if param_1 != 0 else i+3
                continue
            elif opcode == '6':
                i = param_2 if param_1 == 0 else i+3
                continue
            elif opcode == '7':
                program_input[program_input[i+3]] = 1 if param_1 < param_2 else 0
            elif opcode == '8':
                program_input[program_input[i+3]] = 1 if param_1 == param_2 else 0
            i += 4
        elif opcode == '3':
            program_input[program_input[i+1]] = eval(input('Input: '))
            i += 2
        elif opcode == '4':
            print('Output:', program_input[program_input[i+1]])
            i += 2
        j += 1
    return program_input

process_intcode(program_input)

'''
#part 2
found = 0
i = 0
j = 0
while found != 1 and j < 100:
    
    new_input = program_input.copy()
    new_input[1] = i
    new_input[2] = j
    
    output = process_intcode(new_input)

    if output[0] == 19690720:
        found = 1
        print(100*i+j)
    
    i = i + 1
    if i > 99:
        i = 0
        j = j + 1'''