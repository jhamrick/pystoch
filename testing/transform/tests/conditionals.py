# taken from http://wiki.python.org/moin/SimplePrograms

import time
now = time.localtime()
hour = now.tm_hour
if hour < 8: result = 'sleeping'
elif hour < 9: result = 'commuting'
elif hour < 17: result = 'working'
elif hour < 18: result = 'commuting'
elif hour < 20: result = 'eating'
elif hour < 22: result = 'resting'
else: result = 'sleeping'
