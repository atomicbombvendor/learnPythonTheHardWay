from datetime import datetime


def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+1
        n = n + 1

for n in fab(5):
    print n

print 'MonthlyBuilder-{0}-{1}'.format(datetime.now().hour, datetime.now().minute),

pokes=[('7', 2), ('6', 3), ('5', 2), ('4', 1), ('3', 1)]
print pokes[2][0]