import pystoch
from pystoch import flip

result = []
for sample in xrange(SAMPLES):
    result.append(int(flip(0.7)))
exresult = 0.7
