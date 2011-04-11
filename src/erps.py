import random

def flip(weight=0.5):
    return random.uniform(0, 1) <= weight

def uniform(low, high):
    return random.uniform(low, high)
