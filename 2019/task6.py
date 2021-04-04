import math 
with open('puzzle_input/input6.txt') as file:
    puzzle_input = file.read()
    puzzle_input = puzzle_input.split('\n')
    puzzle_input = [x.split(')') for x in puzzle_input]

def find_leaves():
    heads = []
    tails = []
    for obj in puzzle_input:
        if obj[0] not in heads:
            heads.append(obj[0])
    for obj in puzzle_input:
        if obj[1] not in tails:
            tails.append(obj[1])
    return list(set(tails).difference(heads))

def find_all_paths(leaves):
    paths = []
    for leaf in leaves:
        new_path = []
        temp = leaf
        path_complete = False
        while not path_complete:
            new_path.insert(0, temp)
            for obj in puzzle_input:
                if temp == obj[1]:
                    temp = obj[0]
                    break
            else:
                path_complete = True

        paths.append(new_path)        
    return paths


def count_orbits(paths):
    count = 0
    visited = []
    for path in paths:
        for p in path:
            if p not in visited:
                count += path.index(p)
                visited.append(p)
    return count

def find_path(obj_to_find, paths):
    for path in paths:
        if obj_to_find in path:
            return path
    else:
        return None 

def count_transfers(obj1, obj2, paths):
    path1 = find_path(obj1, paths)
    path2 = find_path(obj2, paths)

    common_obj = None
    for i,j in zip(path1, path2):
        if i != j:
            break
        common_obj = i

    transfers = abs(path1.index(obj1) - path1.index(common_obj)) - 1 + abs(path2.index(obj2) - path2.index(common_obj)) - 1
    return transfers

obj1 = 'YOU'
obj2 = 'SAN'

leaves = find_leaves()

paths = find_all_paths(leaves)

print('Part 1:', count_orbits(paths))

print('Part 2:', count_transfers(obj1, obj2, paths))