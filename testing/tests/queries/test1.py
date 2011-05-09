import pystoch
from pystoch.queries import RejectionQuery, MetropolisHastings
from pystoch.erps import flip
from pystoch.graphing import hist

import numpy as np
import datetime

# (define baserate 0.1)
#
# (define samples
#    (mh-query 100 100
#
#        (define A (if (flip baserate) 1 0))
#        (define B (if (flip baserate) 1 0))
#        (define C (if (flip baserate) 1 0))
#        (define D (+ A B C))
#
#        A
#
#        (>= D 2)
#     )
# )


class TestRejectionQuery(RejectionQuery):

    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.baserate = 0.1

    def query_model(self):
        self.A = int(flip(self.baserate))
        self.B = int(flip(self.baserate))
        self.C = int(flip(self.baserate))
        self.D = self.A + self.B + self.C

    def sample(self):
        return self.A

    def condition(self):
        return self.D >= 2

class TestMetropolisHastings(MetropolisHastings):

    def __init__(self):
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.baserate = 0.1

    def query_model(self):
        self.A = int(flip(self.baserate))
        self.B = int(flip(self.baserate))
        self.C = int(flip(self.baserate))
        self.D = self.A + self.B + self.C

    def sample(self):
        return self.A

    def condition(self):
        return self.D >= 2

print "Running rejection query..."
before = datetime.datetime.now()
query1 = TestRejectionQuery()
samples1 = [query1.run() for x in xrange(100)]
after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tResult: %s" % np.mean(samples1)
print "\tTime:   %s seconds" % secs

print "Running metropolis hastings..."
before = datetime.datetime.now()
query2 = TestMetropolisHastings()
samples2 = query2.run(100, 100)
after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tResult: %s" % np.mean(samples2)
print "\tTime:   %s seconds" % secs
