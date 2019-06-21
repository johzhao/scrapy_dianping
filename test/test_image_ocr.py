import os

from PIL import Image
import tesserocr


def test_image_orc():
    folder = './examples'
    for name in os.listdir(folder):
        if not name.endswith('.png'):
            continue

        path = os.path.join(folder, name)
        print(path)

        image = Image.open(path)
        result = tesserocr.image_to_text(image)

        print(result)
