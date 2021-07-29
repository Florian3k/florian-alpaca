from os import path, mkdir
from typing import Optional, Set, Tuple

from PIL import Image
import numpy as np


input_size = 64
upscale_factor = 8
output_size = input_size * upscale_factor


def assert_all_colors_allowed(img: Image.Image, allowed_colors: Optional[Set[Tuple[int, int, int]]] = None):
    if allowed_colors is None:
        allowed_colors = {(255, 255, 255), (0, 0, 0)}

    width, height = img.size
    for y in range(height):
        for x in range(width):
            assert img.getpixel((x, y)) in allowed_colors


if not path.exists('build'):
    mkdir('build')

input_img: Image.Image = Image.open(f'template1_{input_size}x{input_size}.png').convert("RGB")
assert input_img.size == (input_size, input_size)
assert_all_colors_allowed(input_img)

alpaca_color = 83, 83, 83
bg_color = 240, 240, 240
change_colors = [
    ((255, 255, 255), bg_color),
    ((0, 0, 0), alpaca_color)
]

data = np.array(input_img)
r, g, b = data.swapaxes(0, 2).swapaxes(1, 2).copy()

masks_and_colors = [
    (
        (r == from_r) & (g == from_g) & (b == from_b),
        target_color
    )
    for (from_r, from_g, from_b), target_color
    in change_colors
]

for mask, target_color in masks_and_colors:
    data[mask] = target_color

colored_image = Image.fromarray(data)
output_img = colored_image.resize((output_size, output_size), Image.NEAREST)

output_img.save(f"build/florian-alpaca-{output_size}.png")
