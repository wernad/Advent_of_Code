with open('Day 1/input.txt') as file:
    input = file.read()
    input = input.split()
    input = [int(i) for i in input]

#part 1
total = 0
for i in input:
    total += int(i/3)-2

print(total)

#part 2
total = 0
for i in input:
    while i > 0:
        i = int(i/3)-2
        if i <= 0:
            break
        total += i
        

print(total)