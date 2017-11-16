i = 0
numbers = []

while i < 6:
    print "At the top i is %d" % i
    numbers.append(i)
    i += 1
    print "Numbers now: ", numbers
    print "At the bottom i is %d" % i

print "The numbers: "

for num in numbers:
    print num


def print_while():
    t = int(raw_input("T >> "))
    i = 0
    while i < t:
        print "At the top i is %d t is %d" % (i, t)
        numbers.append(i)
        i += 1
        print "Numbers now: ", numbers
        print "At the bottom i is %d" % i


print_while()