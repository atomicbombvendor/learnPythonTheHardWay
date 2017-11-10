# coding=utf-8
name = 'Zed A. Shaw'
age = 35  # not  a lie
height = 74  # inches
weight = 180  # Lbs
eyes = 'Blue'
teeth = 'White'
hair = 'Brown'

print "Let's talk about %s." % name
print "He's %d inches tall." % height
print "He's %f cm tall." % (height * 2.54)
print "He's %d pounds heavy." % weight
print "He's %f kg heavy." % (weight * 0.4535924)
print "Actually that's not too heavy."
print "He's got %s eyes and %s hair." % (eyes, hair)
print "His teeth are usually %s depending on the coffee." % teeth

# this line is tricky, try to get it exactly right
print "If I add %d, %d, and %d I get %d." % (age, height, weight, age + height + weight)

print "If I add %r, %r, and %r I get %r." % (age, height, weight, age + height + weight)
print "%r, %s, %d" % (age, height, weight)
print "%r, %s" % (eyes, eyes)
# %r 可以重现它所代表的对象

x = "There are %d types of people." % 10
binary = "binary"
do_not = "don't"
y = "Those who know %s and those who %s." % (binary, do_not)

print x
print y

print "I said: %r." % x
print "I also said: '%s'." % y

hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

print joke_evaluation % hilarious

w = "This is the left side of"
e = "a string with right side."

print w + e
