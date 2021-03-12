import math
from collections import defaultdict

with open('puzzle_input/input10.txt') as file:
    puzzle_input = file.read().splitlines()
    puzzle_input = [(lambda x: [y for y in x])(x) for x in puzzle_input]
 
def set_coordinates(puzzle_input):
    region_map = []
    x = 0
    y = 0
    for line in puzzle_input:
        new_line = []
        for i in line:
            region_map.append((i, [x, y]))
            x += 1
        y += 1
        x = 0
    return region_map

def find_angles(x, region_map, ret_coords=False):
    angles = []
    for y in region_map:
        if x == y or y[0] == '.':
            continue
        deltaY = x[1][1] - y[1][1]
        deltaX = x[1][0] - y[1][0]
        angle = ((math.degrees(math.atan2(deltaY, deltaX))) - 90) % 360
        if ret_coords:
            angles.append((angle, y[1][0], y[1][1]))
        else:
            angles.append(angle)
    return angles

def find_best_spot(region_map):
    counts = []
    for x in region_map:
        if x[0] == '.':
            continue
        angles = set(find_angles(x, region_map))
        counts.append([len(angles), x[1]])
    return max(counts, key=lambda x: x[0])

def group_by_angle(angles_with_positions, laser_pos):
    def calc_distance(x):
        return ((x[0] - laser_pos[1][0])**2 + (x[1] - laser_pos[1][1])**2)

    new_dict = defaultdict(list)
    for x in angles_with_positions:
        if list(x[1:]) == laser_pos[1]:
            continue
        new_dict[x[0]].append(x[1:])
    for x in new_dict:
        new_dict[x].sort(key=calc_distance)
    return new_dict

def destroy_asteroids(angles_dict):
    count = 0
    current_asteroid = None
    array = []
    while count < 200 and angles_dict != [] :
        angles_dict = {k: v for k, v in angles_dict.items() if v is not None}
        for x in angles_dict:
            if count >= 200:
                break
            array.append(angles_dict[x].pop(0))
            count += 1
    return array[-1] 

region_map = set_coordinates(puzzle_input)

#Part 1
best_spot = find_best_spot(region_map)

#Part 2
asteroids_with_angles = sorted(find_angles(best_spot, region_map, True), key=lambda x: x[0])
asteroids_grouped_by_angles = group_by_angle(asteroids_with_angles, best_spot)
asteroid_no_200 = destroy_asteroids(asteroids_grouped_by_angles)

print('Part 1:', best_spot[0])
print('Part 2:', asteroid_no_200[0] * 100 + asteroid_no_200[1])