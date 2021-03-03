from collections import Counter
import numpy as np
with open('puzzle_input/input8.txt') as file:
    puzzle_input = file.read()
    puzzle_input = np.array([int(i) for i in str(puzzle_input)])

image_width = 25
image_height = 6
image_layer_count = int(len(puzzle_input)/(image_height * image_width))

image_layers = puzzle_input.reshape(image_layer_count, image_height * image_width)
def check_image(image_layers):
    digit_frequency = [dict(zip(*np.unique(x, return_counts=True))) for x in image_layers]
    zeroes_frequency = [x[0] for x in digit_frequency]
    layer_index = zeroes_frequency.index(min(zeroes_frequency))
    return digit_frequency[layer_index][1] * digit_frequency[layer_index][2]

def draw_image(image_layers, image_height, image_width):
    image = []
    for x in range(image_height * image_width):
        for layer in image_layers:
            if layer[x] == 2:
                continue
            elif layer[x] == 1:
                image.append(1)
                break
            elif layer[x] == 0:
                image.append(0)
                break
    return np.array(image).reshape(6,25)

print('Part 1:', check_image(image_layers))
print('Part 2:\n', draw_image(image_layers, image_height, image_width))
