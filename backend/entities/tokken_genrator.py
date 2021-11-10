import string
import random


def get_tokken(tokken_length=40):
    possible_char = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join((random.choice(possible_char) for x in range(tokken_length)))
    # return ''.join((random.choice(string.printable[:-6]) for x in range(tokken_length)))
