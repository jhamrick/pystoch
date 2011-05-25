# from http://wiki.python.org/moin/SimplePrograms

parents, babies = (1, 1)
result = []
while babies < 100:
    result.append('This generation has %d babies' % babies)
    parents, babies = (babies, parents + babies)
