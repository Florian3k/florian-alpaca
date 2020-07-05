from os import path, mkdir
from typing import Optional, Set, Tuple

from PIL import Image
import numpy as np


def assert_all_colors_allowed(img: Image.Image, allowed_colors: Optional[Set[Tuple[int, int, int]]] = None):
    if allowed_colors is None:
        allowed_colors = {(255, 255, 255), (0, 0, 0)}

    width, height = img.size
    for y in range(height):
        for x in range(width):
            assert img.getpixel((x, y)) in allowed_colors


if not path.exists('build'):
    mkdir('build')

input_img: Image.Image = Image.open('template1_64x64.png').convert("RGB")
assert input_img.size == (64, 64)
assert_all_colors_allowed(input_img)

change_colors = [
    ((255, 255, 255), (255, 255, 255)),  # background color
    ((0, 0, 0), (53, 53, 53))  # alpaca color
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
output_img = colored_image.resize((512, 512), Image.NEAREST)
assert_all_colors_allowed(output_img, {(255, 255, 255), (53, 53, 53)})

output_img.save("build/florian-alpaca.png")
