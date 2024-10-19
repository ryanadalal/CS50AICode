import cv2
import numpy as np
import os
import sys

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    print(type(images))
    print(type(images.pop()))
    print(images.pop().shape)
    print(images.pop().dtype)

def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    for i in range(0, NUM_CATEGORIES):
        for imgfile in os.listdir(os.path.join(data_dir, str(i))):
            img = cv2.imread(os.path.join(data_dir, str(i), imgfile), )
            img.resize(IMG_WIDTH, IMG_HEIGHT, 3)
            images.append(img)
            labels.append(i)

    return (images, labels)


if __name__ == "__main__":
    main()
