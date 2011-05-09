from queries import RejectionQuery
from erps import flip
from graphing import hist
import numpy as np

class ShortTest(RejectionQuery):

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

query = ShortTest()
samples = [query.run() for x in xrange(100)]

print samples
print np.mean(samples)

hist(samples, "Value of A, given that D is greater than or equal to 2")
