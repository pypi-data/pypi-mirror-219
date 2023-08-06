import numpy as np


def count_in_list(l, word):
    """
    counter
    """
    counter = 0
    for item in l:
        if item == word:
            counter += 1
    return counter


def add(x, y):
    return x+y


def multiply(x, y):
    return x*y


def array_maker(tuple):
    return np.array(tuple)

