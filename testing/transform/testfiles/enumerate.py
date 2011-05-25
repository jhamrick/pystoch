# taken from http://wiki.python.org/moin/SimplePrograms

my_list = ['john', 'pat', 'gary', 'michael']
result = []
for i, name in enumerate(my_list):
    result.append("iteration %i is %s" % (i, name))
