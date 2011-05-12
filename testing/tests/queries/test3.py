import pystoch
from pystoch.queries import RejectionQuery, MetropolisHastings
from pystoch.erps import flip
from pystoch.graphing import discrete_hist

import numpy as np
import datetime
import pdb

# (define samples
#    (mh-query 1000 100
#         (define lung-cancer (flip 0.01))
#         (define TB (flip 0.005))
#         (define cold (flip 0.2))
#         (define stomach-flu (flip 0.1))
#         (define other (flip 0.1))
#
#         (define cough (or (and cold (flip 0.5)) (and lung-cancer (flip 0.3)) (and TB (flip 0.7)) (and other (flip 0.01))))
#         (define fever (or (and cold (flip 0.3)) (and stomach-flu (flip 0.5)) (and TB (flip 0.2)) (and other (flip 0.01))))
#         (define chest-pain (or (and lung-cancer (flip 0.4)) (and TB (flip 0.5)) (and other( flip 0.01))))
#         (define shortness-of-breath (or (and lung-cancer (flip 0.4)) (and TB (flip 0.5)) (and other (flip 0.01))))
#
#            (list lung-cancer TB)
#
#         (and cough fever chest-pain shortness-of-breath)
#
#       )
#  )

class Test(MetropolisHastings):

    def __init__(self):
        self.lung_cancer = None
        self.TB = None
        self.cold = None
        self.stomach_flu = None
        self.other = None
        
        self.cough = None
        self.fever = None
        self.chest_pain = None
        self.shortness_of_breath = None

    def query_model(self):
        self.lung_cancer = flip(0.01)
        self.TB = flip(0.005)
        self.cold = flip(0.2)
        self.stomach_flu = flip(0.1)
        self.other = flip(0.1)

        self.cough = (self.cold and flip(0.5)) or \
                     (self.lung_cancer and flip(0.3)) or \
                     (self.TB and flip(0.7)) or \
                     (self.other and flip(0.01))
        
        self.fever = (self.cold and flip(0.3)) or \
                     (self.stomach_flu and flip(0.5)) or \
                     (self.TB and flip(0.2)) or \
                     (self.other and flip(0.01))

        self.chest_pain = (self.lung_cancer and flip(0.4)) or \
                          (self.TB and flip(0.5)) or \
                          (self.other and flip(0.01))

        self.shortness_of_breath = (self.lung_cancer and flip(0.4)) or \
                                   (self.TB and flip(0.5)) or \
                                   (self.other and flip(0.01))

    def sample(self):
        return self.lung_cancer, self.TB

    def condition(self):
        return self.cough and self.fever and self.chest_pain and self.shortness_of_breath

num_samples = 1000

print "Running metropolis hastings..."
before = datetime.datetime.now()
query = Test()
samples = [str(samp) for samp in query.run(num_samples, 100)]
after = datetime.datetime.now()
td = after - before
secs = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6
secs = np.round(secs, decimals=2)
print "\tTime:   %s seconds" % secs
print

discrete_hist(samples, "Joint Inferences for Lung Cancer and TB",
              path="../../../test3.pdf")
