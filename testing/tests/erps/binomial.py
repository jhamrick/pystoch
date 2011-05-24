import pystoch
from pystoch import RejectionQuery, MetropolisHastings, binomial, hist

import datetime
import numpy as np
import scipy.stats

class Test(object):

    def __init__(self):
        self.val = None

    def query_model(self):
        self.val = binomial(20, 0.8)

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

hist(np.array([samples1, samples2]), "Binomial Distribution (n=20, p=0.8)",
     labels=["RejectionQuery",
             "MetropolisHastings"],
     path="../../../graphs/binomial.pdf")
