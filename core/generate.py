import random


def generate_otp(length=6):
    otp = ""
    for _ in range(length):
        otp += str(random.randint(0, 9))
    return otp

def generate_username(name):
    pass