import random


def random_hex():
    chars = '0123456789ABCDEF'
    hx = '#'
    for i in range(6):
        hx += random.choice(chars)
    return hx
