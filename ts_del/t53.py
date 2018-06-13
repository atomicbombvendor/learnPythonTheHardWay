def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+1
        n = n + 1

for n in fab(5):
    print n