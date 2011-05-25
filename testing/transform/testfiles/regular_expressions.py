# taken from http://wiki.python.org/moin/SimplePrograms

import re
result = []
for test_string in ['555-1212', 'ILL-EGAL']:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        result.append(test_string + ' is a valid US local phone number')
    else:
        result.append(test_string + 'rejected')
