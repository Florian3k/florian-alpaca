from os import path, mkdir
from typing import Optional, Set, Tuple

from PIL import Image


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

output_img = input_img.resize((512, 512), Image.NEAREST)
assert_all_colors_allowed(output_img)

output_img.save("build/test1.png")
