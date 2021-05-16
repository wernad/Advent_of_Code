import math 
with open('puzzle_input/input6.txt') as file:
    puzzle_input = file.read()
    puzzle_input = puzzle_input.split('\n')
    puzzle_input = [x.split(')') for x in puzzle_input]

#Finds leaves of tree structure of orbiting objects.
def find_leaves():
    heads = [] #Orbited object
    tails = [] #Orbiting object
    for obj in puzzle_input:
        if obj[0] not in heads:
            heads.append(obj[0])
        if obj[1] not in tails:
            tails.append(obj[1])
    return list(set(tails).difference(heads))

#Build paths from leaf to root via traversing dictionary.
def find_all_paths(leaves, puzzle_input):
    leaves_to_root = {v:k for k,v in puzzle_input}
    paths = []
    for leaf in leaves:
        new_path = [leaf]
        while new_path[-1] in leaves_to_root:
            new_path.append(leaves_to_root[new_path[-1]])
        new_path.reverse()
        paths.append(new_path)
    return paths

def count_orbits(paths):
    count = 0
    visited = []
    for path in paths:
        for i, p in enumerate(path):
            if p not in visited:
                count += i #Adds index because number of orbits of an object is a sum of all previous orbits.
                visited.append(p)
    return count

def find_path(obj_to_find, paths):
    for path in paths:
        if obj_to_find in path:
            return path
    return None 

def count_transfers(start, end, paths):
    path1 = find_path(start, paths)
    path2 = find_path(end, paths)

    #Finds common object that is orbited by both objects.
    common_obj = None
    for i,j in zip(path1, path2):
        if i != j:
            break
        common_obj = i

    # Subtract 1 because we want to get to the objects orbiting around start and end, not objects themselves.
    transfers = abs(path1.index(start) - path1.index(common_obj)) - 1 + abs(path2.index(end) - path2.index(common_obj)) - 1
    return transfers

obj1 = 'YOU'
obj2 = 'SAN'

leaves = find_leaves()

paths = find_all_paths(leaves, puzzle_input)

print('Part 1:', count_orbits(paths))

print('Part 2:', count_transfers(obj1, obj2, paths))