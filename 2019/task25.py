import intcode_computer as ic
import re
puzzle_input = ic.load_input('25')

droid = ic.IntcodeComputer(puzzle_input, True, True)

right_answer = '''east
take sand
west
west
north
take wreath
east
take fixed point
west
south
south
east
take escape pod
west
south
east
east
south
take photons
west
south
east
east
east
take space law space brochure
south
south
west
'''

def play():
    while True:
        while droid.process_intcode() != -1 and droid.turned_on:
            continue
        output = droid.ASCII2list(droid.output)
        print(''.join(output))
        user_input = input()
        command = droid.list2ASCII(user_input)
        droid.input = command

def solve(): # Sand, Fixed point, Escape pod, Photons, Space Law Space Brochure, Wreath
    droid.input = droid.list2ASCII(right_answer)

    output = ''
    while not re.search(r'\d{8}',output):
        droid.process_intcode()
        output = ''.join(droid.ASCII2list(droid.output))

    print('Part 1:', re.findall(r'\d{8}', output)[0])

while True:
    print('Pick mode:\n  1 - play game\n  2 - auto solve game')
    mode = input('Your choice: ')
    if mode == '1':
        play()
        break
    elif mode == '2':
        solve()
        break
    else:
        print('Incorrect mode. Try again.')
