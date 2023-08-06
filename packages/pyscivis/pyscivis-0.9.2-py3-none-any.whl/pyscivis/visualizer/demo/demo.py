import glob
import os

from PIL import Image
import numpy as np


def get_images(width, height):
    """
    Collect all png-images in the same folder as this script, resize them and convert them to numpy-arrays.

    Args:
        width: Width for images.
        height: Height for images.

    Returns:
        3-dimensional numpy-array with shape (image-count, height, width).
    """
    image_paths = glob.glob(os.path.join(os.path.dirname(__file__), "*.png"))
    image_series = []
    img: Image.Image
    for i, p in enumerate(image_paths):
        with Image.open(p) as img:
            img = img.resize((width, height)).convert('L')
            image_series.append(np.asarray(img))

    return np.array(image_series)


if __name__ == "__main__":
    print(get_images(100, 200).shape)
