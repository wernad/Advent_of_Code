from itertools import tee, groupby

#https://docs.python.org/3/library/itertools.html#recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
    
def check_accend(number):
    for a,b in pairwise(number):
        if a > b:
            return False
    return True


MIN_RANGE = 357253
MAX_RANGE = 892942

count = 0
isolated_count = 0
for i in range(MIN_RANGE, MAX_RANGE):
    i = str(i)
        
    if not check_accend(i):
        continue

    groups = []
    for _, g in groupby(i):
        groups.append(len(list(g)))
    
    if max(groups) < 2:
        continue
    
    count += 1

    if 2 not in groups:
        continue
    
    isolated_count += 1

print('Part 1:', count)
print('Part 2:', isolated_count)