from collections import defaultdict
from math import ceil

with open('puzzle_input/input14.txt') as file:
    puzzle_input = [x.split(' => ') for x in file.read().splitlines()]
    puzzle_input = [(lambda x: (x[0].split(','), x[1]))(x)for x in puzzle_input]
    puzzle_input = {x[1].split()[1] : (x[0],int(x[1].split()[0])) for x in puzzle_input}

def set_complexity_levels():
    global recipes
    complexity_levels = dict({'ORE' : 0})
    level = 1
    while len(recipes) >= len(complexity_levels):
        new_levels = {}
        for chem in recipes:
            if chem in complexity_levels:
                continue
            if all(x in complexity_levels for x in recipes[chem][0]):
                new_levels[chem] = level
        level += 1
        complexity_levels.update(new_levels)
        
    return complexity_levels

def find_ore_req(product):
    global recipes, complexity_levels
    chemicals = defaultdict(int, product)
    while 'ORE' not in chemicals or len(chemicals) > 1:
        chem = max(chemicals, key=lambda x: complexity_levels[x])
        required_amount = chemicals[chem]
        del chemicals[chem]

        ingredients, produced_amount = recipes[chem]
        
        multiplier = ceil(required_amount/produced_amount)

        for i in ingredients:
            chemicals[i] += (ingredients[i] * multiplier)
            
    return chemicals['ORE']

def max_fuel(low,high):
    global stored_ore
    current_value = find_ore_req({'FUEL': low})
    while high - low != 1:
        mid = (high + low)//2
        current_value = find_ore_req({'FUEL': mid})

        if current_value > stored_ore:
            high = mid
        else:
            low = mid

    return mid

recipes = dict()
for k,v in puzzle_input.items():
    new_dict = dict()
    for x in v[0]:
        new_dict[x.split()[1]] = int(x.split()[0])
    recipes[k] = (new_dict, v[1])

complexity_levels = set_complexity_levels()
ore_count = find_ore_req({'FUEL': 1})

stored_ore = 1000000000000
low = 1
high = 2000000

print('Part 1', ore_count)
print('Part 2:', max_fuel(low, high))

#simple_chemicals = find_simple_chemicals({'FUEL':1})
#print(chem2ore(simple_chemicals))

""" Bad approach
def find_simple_chemicals(product):
    global recipes, complexity_levels
    chemicals = defaultdict(int, product)
    final_reaction = defaultdict(int)
    while chemicals:
        new_chemicals = defaultdict(int)
        chemicals = dict(sorted(chemicals.items(), key=lambda x: complexity_levels[x[0]], reverse=True))
        print(chemicals)
        for chem in chemicals:
            top_level_chem = max(chemicals, key=lambda x: complexity_levels[x])
            if complexity_levels[chem] < complexity_levels[top_level_chem]:
                #print(chem, complexity_levels[chem], '<<<', max(chemicals, key=lambda x: complexity_levels[x]), complexity_levels[max(chemicals, key=lambda x: complexity_levels[x])])
                new_chemicals[chem] = chemicals[chem]
                continue
            print(chem, complexity_levels[chem])
            chem_required = chemicals[chem]
            ingredients, produced_amount = recipes[chem]
            multiplier = ceil(chem_required/produced_amount)
            for i in ingredients:
                if i == 'ORE':
                    final_reaction[chem] += (chem_required * multiplier)
                else:
                    new_chemicals[i] += (ingredients[i] * multiplier)
        chemicals = new_chemicals
    #print(final_reaction)
    return final_reaction

def chem2ore(chemicals):
    ore_count = 0
    for chem in chemicals:
        chem_required = chemicals[chem]
        ingredients, produced_amount = recipes[chem]
        multiplier = ceil(chem_required/produced_amount)
        ore_count += (produced_amount * multiplier)
    return ore_count
"""