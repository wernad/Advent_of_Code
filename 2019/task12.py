from itertools import combinations

with open('puzzle_input/input12.txt') as file:
    puzzle_input = file.read()
    puzzle_input =  puzzle_input.replace('<', '').replace('>', '').replace(',', '').split('\n')

def calc_movement(coords, velocities, moons_comb):
    for x in moons_comb:
        for j in range(3):
            if coords[x[0]][j] > coords[x[1]][j]:
                velocities[x[0]][j] -= 1
                velocities[x[1]][j] += 1
            elif coords[x[0]][j] < coords[x[1]][j]:
                velocities[x[0]][j] += 1
                velocities[x[1]][j] -= 1
    for j in range(len(coords)):
        coords[j] = [sum(x) for x in zip(coords[j], velocities[j])]    
    
    return coords, velocities

coords = [(lambda x: [int(y[2:]) for y in x.split()])(x) for x in puzzle_input]
velocities = [[0]*3 for _ in range(4)]
moons_comb = list(combinations(range(len(coords)), 2))

i = 0
new_coords = []
new_velocities = []
while i < 1000:
    new_coords, new_velocities = calc_movement(coords, velocities, moons_comb)
    i += 1
pot = [sum(y) for y in [map(abs, x) for x in new_coords]]
kin = [sum(y) for y in [map(abs, x) for x in new_velocities]]
print('Part 1:', sum([a*b for a,b in zip(pot, kin)]))