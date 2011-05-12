import pystoch
from pystoch.queries import MetropolisHastings
from pystoch.erps import flip, uniform
from pystoch.graphing import cont_hist

import numpy as np
import datetime
import pdb

# (define observed-data '(h h h h h))
# (define num-flips (length observed-data))
# (define num-samples 1000)
# (define prior-samples (repeat num-samples (lambda () (uniform 0 1))))

# (define samples
#    (mh-query
#          num-samples 10

#          (define coin-weight (uniform 0 1))

#          (define make-coin (lambda (weight) (lambda () (if (flip weight) 'h 't))))
#          (define coin (make-coin coin-weight))

#          coin-weight

#               (equal? observed-data (repeat num-flips coin))
#        )
#  )

# (truehist (append '(0) '(1) prior-samples) 10 "Coin weight, prior to observing data")
# (truehist (append '(0) '(1) samples) 10 "Coin weight, conditioned on observed data")

class Test(MetropolisHastings):

    def __init__(self):
        self.observed_data = ['H', 'H', 'H', 'H', 'H']
        self.num_flips = len(self.observed_data)

        self.coin_weight = None

    def coin(self, weight):
        if flip(weight):
            return 'H'
        return 'T'

    def query_model(self):
        self.coin_weight = uniform(0, 1)
        self.sampled_data = [self.coin(self.coin_weight) for i in xrange(self.num_flips)]

    def sample(self):
        return self.coin_weight

    def condition(self):
        return self.observed_data == self.sampled_data


num_samples = 1000

print "Running metropolis hastings..."
before = datetime.datetime.now()
query = Test()

prior_samples = [np.random.uniform(0, 1) for sample in xrange(num_samples)]
samples = query.run(num_samples, 100)

after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tTime:   %s seconds" % secs
print

cont_hist(np.array([prior_samples, samples]), "Beliefs about Coin Weight",
          numbins=20,
          labels=["prior to observing data",
                  "conditioned on observed data"],
          path="../../../graphs/test4.pdf")
                   
