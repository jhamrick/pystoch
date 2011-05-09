import pystoch
from pystoch.queries import RejectionQuery, MetropolisHastings
from pystoch.erps import flip
from pystoch.graphing import hist

import numpy as np
import datetime

# (define samples
#   (mh-query 100 100
#       (define breast-cancer (flip 0.01))
#
#       (define positive-mammogram (if breast-cancer (flip 0.8) (flip 0.096)))
#
#       breast-cancer
#
#       positive-mammogram
#     )
#  )

class Test(object):

    def __init__(self):
        self.breast_cancer = None
        self.positive_mammogram = None

    def query_model(self):
        self.breast_cancer = flip(0.01)

        if self.breast_cancer:
            self.positive_mammogram = flip(0.8)
        else:
            self.positive_mammogram = flip(0.096)

    def sample(self):
        return self.breast_cancer

    def condition(self):
        return self.positive_mammogram

class TestRejectionQuery(RejectionQuery, Test):
    def __init__(self):
        Test.__init__(self)
class TestMetropolisHastings(MetropolisHastings, Test):
    def __init__(self):
        Test.__init__(self)

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

