import re

with open('puzzle_input/input22.txt') as file:
    puzzle_input = [x.strip('\n')for x in file.readlines()]

def shuffle(deck):
    global puzzle_input
    for technique in puzzle_input:
        func, param = re.search(r'((?:[a-z]+ ?)+)(-?\d+)?', technique).groups()
        func = re.sub(r'\s$', '', func)
        if func == 'cut':
            param = int(param)
            deck = deck[param:] + deck[:param]
        elif func == 'deal with increment':
            param = int(param)
            new_deck = [0] * len(deck)
            index = 0
            for card in deck:
                new_deck[index%len(deck)] = card
                index += param        
            deck = new_deck
        else:
            deck = list(reversed(deck))
    return deck

deck_size = 10007
deck = list(range(deck_size))

print('Part 1:', shuffle(deck).index(2019))
