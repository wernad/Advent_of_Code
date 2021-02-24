with open('puzzle_input/input1.txt') as file:
    input = file.read()
    input = input.split()
    input = [int(i) for i in input]

#part 1
total = 0
for i in input:
    total += int(i/3)-2

print('Part 1:', total)

#part 2
total = 0
for i in input:
    while i > 0:
        i = int(i/3)-2
        if i <= 0:
            break
        total += i
        

print('Part 2:', total)