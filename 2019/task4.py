from itertools import tee
import more_itertools
import copy

min_range = 357253
max_range = 892942

def tripletwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    c = copy.copy(b)
    next(c, None)
    return zip(a,b,c)
    

count = 0
isolated_count = 0
for i in range(min_range, max_range):
    double_found = 0
    isolated_double_found = 0    
    incremental = 1
    last_a = -1
    for a, b, c in tripletwise(str(i)):
        if int(a) > int(b) or int(b) > int(c):
            incremental = 0
            break
        if a == b or b == c: #part 1
            double_found = 1
        if a == b == c: #part 2
            pass
        elif a == b and a != last_a:
            isolated_double_found = 1
        last_a = a
    else:
        if a != b and b == c:
            isolated_double_found = 1
    if double_found == 1 and incremental == 1:
        count += 1
    if isolated_double_found == 1 and incremental == 1:
        isolated_count += 1

print(count)

print(isolated_count)