from numpy import random


def get_random_value_from_normal(mean: float, std: float):
    """ Gets a random number from mean and standard deviation """
    return int(random.normal(mean, std, 1))
