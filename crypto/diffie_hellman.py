import random

def generate_private_key(p):
    return random.randint(2, p-2)

def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

def compute_shared_secret(their_public, my_private, p):
    return pow(their_public, my_private, p)


