import numpy as np

def calculate_area(length, width):
    length = np.float32(length) / 255
    return length * width

def calculate_perimeter(length, width):
    return 2 * (length + width)