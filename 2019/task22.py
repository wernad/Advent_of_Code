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

#Transformations in a form of linear congruential function.
def shuffle_lcf(deck_size):
    global puzzle_input
    a,b = 1,0
    for technique in puzzle_input:
        func, param = re.search(r'((?:[a-z]+ ?)+)(-?\d+)?', technique).groups()
        func = re.sub(r'\s$', '', func)
        if func == 'cut':
            param = int(param)
            new_a, new_b = 1, -param
        elif func == 'deal with increment':
            param = int(param)
            new_a, new_b = param, 0
        else: #into stack
            new_a, new_b = -1, -1
        a = new_a * a % deck_size
        b = (new_a * b + new_b) % deck_size
    return a,b

#Title: Exponentiation by squaring
#Author: Spheniscine
#Date: 2019
#Availability: https://codeforces.com/blog/entry/72527
def pow_mod(x, n, m):
    y = 1
    while n > 0:
        if n % 2 != 0:
            y = y * x % m
        x = x * x % m
        n //= 2
    return y

#Title: Modified Exponentiation by squaring
#Author: Spheniscine
#Date: 2019
#Availability: https://codeforces.com/blog/entry/72593
def pow_compose(f, k, m):
    def compose(f, g, m):
        a,b = f
        c,d = g
        return (a * c % m, (b * c + d) % m)

    g = (1,0)
    while k > 0:
        if k % 2 != 0:
            g = compose(g, f, m)
        f = compose(f,f, m)
        k //= 2
    return g

deck_size = 10007
deck = list(range(deck_size))

deck_size = 119315717514047
repeat = 101741582076661

a, b =  shuffle_lcf(deck_size)

f = (a,b)
A, B = pow_compose(f, repeat, deck_size)

print('Part 1:', shuffle(deck).index(2019))
print('Part 2:', (2020 - B) * pow_mod(A, deck_size - 2, deck_size) % deck_size)
