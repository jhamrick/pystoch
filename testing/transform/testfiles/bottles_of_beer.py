# taken from http://wiki.python.org/moin/SimplePrograms

REFRAIN = '''
%d bottles of beer on the wall,
%d bottles of beer,
take one down, pass it around,
%d bottles of beer on the wall!
'''
bottles_of_beer = 99
result = []
while bottles_of_beer > 1:
    result.append(REFRAIN % (bottles_of_beer, bottles_of_beer,
                             bottles_of_beer - 1))
    bottles_of_beer -= 1
