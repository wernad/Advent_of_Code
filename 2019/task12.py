from itertools import combinations
from math import gcd
import copy

with open('puzzle_input/input12.txt') as file:
    puzzle_input = file.read()
    puzzle_input =  [(lambda x: [int(y[2:]) for y in x.split()])(x) for x in puzzle_input.replace('<', '').replace('>', '').replace(',', '').split('\n')]

def calc_energy(values):
    return [sum(y) for y in [map(abs, x) for x in values]]

def calc_movement(positions, velocities, moons_comb):
    for x in moons_comb:
        for j in range(3):
            if positions[x[0]][j] > positions[x[1]][j]:
                velocities[x[0]][j] -= 1
                velocities[x[1]][j] += 1
            elif positions[x[0]][j] < positions[x[1]][j]:
                velocities[x[0]][j] += 1
                velocities[x[1]][j] -= 1
    for j in range(len(positions)):
        positions[j] = [sum(x) for x in zip(positions[j], velocities[j])]    
    
    return positions, velocities

def find_axis_periods(positions, velocities, moons_comb):
    orig_positions = copy.deepcopy(positions)
    orig_velocities = copy.deepcopy(velocities)
    periods = []
    
    for i in range(3):
        start_pos = [x[i] for x in positions]
        count = 0
        while True:                
            positions, velocities = calc_movement(positions, velocities, moons_comb)
            count += 1
            if [x[i] for x in positions] == start_pos and [x[i] for x in velocities] == [0,0,0,0]:
                break
                
        periods.append(count)
        positions = copy.deepcopy(orig_positions)
        velocities = copy.deepcopy(orig_velocities)
    return periods 

def lcm(numbers):
    while len(numbers) > 1:
        a = numbers.pop()
        b = numbers.pop()
        numbers.append((a*b)//gcd(a,b))
    return numbers[-1]

positions = copy.deepcopy(puzzle_input)
velocities = [[0]*3 for _ in range(len(positions))]
moons_combinations = list(combinations(range(len(positions)), 2))

for i in range(1000):
    positions, velocities = calc_movement(positions, velocities, moons_combinations)

potential_energy = calc_energy(positions)
kinetic_energy = calc_energy(velocities)

positions = copy.deepcopy(puzzle_input)
velocities = [[0]*3 for _ in range(len(positions))]

periods = find_axis_periods(positions, velocities, moons_combinations)

print('Part 1:', sum([a*b for a,b in zip(potential_energy, kinetic_energy)]))
print('Part 2:', lcm(periods))