things = ['a', 'b', 'c', 'd']
print things[1]

things[1] = 'z'
print things[1]

print things

stuff = {'name':'zed', 'age':36, 'height':6*12+2}
print stuff['name']

print stuff['name']

print stuff['age']

print stuff['height']

stuff[1] = 'Wow'
print stuff[1]

stuff[2] = 'Neato'
print stuff[2]

stuff["t"] = 'T'
print stuff["t"]

print stuff

del stuff['t']

del stuff[1]

#############
cities = {'CA':"San Francisco", 'MI':'Detroit', 'FL':'JacksonVille'}

cities['NY'] = 'New York'
cities['OR'] = 'Portland'

def print_city(themap):
    for city in themap.items():
        print city,

def print_city2(themap):
    for city in themap:
        print city,

print "Now print items"
print_city(cities)

print "\nNow print dicts"
print_city2(cities)

def find_city(themap, state):
    if state in themap:
        return themap[state]
    else:
        return "Not found."

# OK pay attention!
cities['_find'] = find_city

while True:
    print "\nState? (Enter to quit)",
    state = raw_input("> ")
    if not state: break

    # this line is the most important ever! study!
    city_found = cities['_find'](cities, state)
    print city_found