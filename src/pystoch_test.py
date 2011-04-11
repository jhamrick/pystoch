import matplotlib.pyplot as plt
from queries import RejectionQuery
from erps import flip, uniform
import numpy as np

class CausalInductionQuery(RejectionQuery):

    def __init__(self, e_given_c, e_given_notc, num_c, draw_e):
        self.e_given_c = e_given_c
        self.e_given_notc = e_given_notc
        self.num_c = num_c
        self.draw_e = draw_e

        self.w0 = None
        self.w1 = None
        self.c_causes_e = None
        self.rate_true_positive = None
        self.rate_false_positive = None

    def sample_positives(self, is_true):
        samples = []
        for i in xrange(self.num_c):
            samples.append(self.draw_e(is_true, self.c_causes_e, self.w0, self.w1))
        return np.mean(samples)

    def query_model(self):
        self.w0 = uniform(0, 1)
        self.w1 = uniform(0, 1)
        self.c_causes_e = flip()
        self.rate_true_positive = self.sample_positives(True)
        self.rate_false_positive = self.sample_positives(False)

    def query(self):
        return self.c_causes_e, self.w1

    def condition(self):
        return (self.rate_true_positive == self.e_given_c) and \
               (self.rate_false_positive == self.e_given_notc)

def noisy_OR(c, c_causes_e, w0, w1):
    if c_causes_e:
        return flip(w0) or (c and flip(w1))
    else:
        return flip(w0)

def noisy_AND_NOT(c, c_causes_e, w0, w1):
    if c_causes_e:
        return flip(w0) and not (c and flip(w1))
    else:
        return flip(w0)

def generic(c, c_causes_e, w0, w1):
    if c_causes_e and c:
        return flip(w1)
    else:
        return flip(w0)

contingencies = [
    (1.0, 1.0),
    (0.75, 0.75),
    (0.5, 0.5),
    (0.25, 0.25),
    (0.0, 0.0),
    (1.0, 0.75),
    (0.75, 0.5),
    (0.5, 0.25),
    (0.25, 0.0),
    (1.0, 0.5),
    (0.75, 0.25),
    (0.5, 0.0),
    (1.0, 0.25),
    (0.75, 0.0),
]

num_samples = 100

noisy_or_means = []
for e_given_c, e_given_notc in contingencies:
    print "Running queries for %s, %s ..." % (e_given_c, e_given_notc)
    rejquery = CausalInductionQuery(e_given_c, e_given_notc, 8, noisy_OR)
    noisy_or_means.append(np.mean([rejquery.sample()[0] for x in range(num_samples)]))

noisy_and_not_means = []
for e_given_c, e_given_notc in contingencies:
    print "Running queries for %s, %s ..." % (e_given_c, e_given_notc)
    rejquery = CausalInductionQuery(e_given_c, e_given_notc, 8, noisy_AND_NOT)
    noisy_and_not_means.append(np.mean([rejquery.sample()[0] for x in range(num_samples)]))

generic_means = []
for e_given_c, e_given_notc in contingencies:
    print "Running queries for %s, %s ..." % (e_given_c, e_given_notc)
    rejquery = CausalInductionQuery(e_given_c, e_given_notc, 8, generic)
    generic_means.append(np.mean([rejquery.sample()[0] for x in range(num_samples)]))

print noisy_or_means
print noisy_and_not_means
print generic_means
