import pystoch
from pystoch.queries import RejectionQuery, MetropolisHastings
from pystoch.erps import exponential
from pystoch.graphing import cont_hist

import datetime
import numpy as np

class Test(object):

    def __init__(self):
        self.val = None

    def query_model(self):
        self.val = exponential(0.5)

    def sample(self):
        return self.val

    def condition(self):
        return True


class TestRejectionQuery(RejectionQuery, Test):
    def __init__(self):
        Test.__init__(self)
class TestMetropolisHastings(MetropolisHastings, Test):
    def __init__(self):
        Test.__init__(self)

num_samples = 1000

print "Running rejection query..."
before = datetime.datetime.now()
query1 = TestRejectionQuery()
samples1 = [query1.run() for x in xrange(num_samples)]
after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tResult: %s" % np.mean(samples1)
print "\tTime:   %s seconds" % secs

print "Running metropolis hastings..."
before = datetime.datetime.now()
query2 = TestMetropolisHastings()
samples2 = query2.run(num_samples, 10)
after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tResult: %s" % np.mean(samples2)
print "\tTime:   %s seconds" % secs

cont_hist(np.array([samples1, samples2]), "Exponential (lambda=0.5)",
          numbins=20,
          labels=["RejectionQuery", "MetropolisHastings"],
          path="../../../graphs/exponential.pdf")
