import string
import random


def get_tokken(tokken_length=80):
    possible_char = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%()*+,-.:<>@[]^_{|}~"
    return ''.join((random.choice(possible_char) for x in range(tokken_length)))
