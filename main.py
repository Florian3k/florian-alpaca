from os import path, mkdir
from PIL import Image


def assert_all_black_white(img: Image.Image):
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            assert r == g == b
            assert r == 0 or r == 255


if not path.exists('build'):
    mkdir('build')

input_img: Image.Image = Image.open('template1_64x64.png').convert("RGB")
assert input_img.size == (64, 64)
assert_all_black_white(input_img)

output_img = input_img.resize((512, 512), Image.NEAREST)
assert_all_black_white(output_img)

output_img.save("build/test1.png")
