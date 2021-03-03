with open('puzzle_input/input1.txt') as file:
    puzzle_input = file.read()
    puzzle_input = puzzle_input.split()
    puzzle_input = [int(i) for i in puzzle_input]

#part 1
total = 0
for i in puzzle_input:
    total += int(i/3)-2

print('Part 1:', total)

#part 2
total = 0
for i in puzzle_input:
    while i > 0:
        i = int(i/3)-2
        if i <= 0:
            break
        total += i
        

print('Part 2:', total)