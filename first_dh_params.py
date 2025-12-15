import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_prime(bits=16):
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if is_prime(p):
            return p

def prime_factors(n):
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors

def find_primitive_root(p):
    if p == 2:
        return 1
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        flag = False
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                flag = True
                break
        if not flag:
            return g
    return None

def generate_dh_params(bits=16):
    p = generate_prime(bits)
    g = find_primitive_root(p)
    return p, g
