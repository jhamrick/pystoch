# taken from http://wiki.python.org/moin/SimplePrograms

import itertools
lines = '''
This is the
first paragraph.

This is the second.
'''.splitlines()

# Use itertools.groupby and bool to return groups of
# consecutive lines that either have content or don't.
result = []
for has_chars, frags in itertools.groupby(lines, bool):
    if has_chars:
        result.append(' '.join(frags))
