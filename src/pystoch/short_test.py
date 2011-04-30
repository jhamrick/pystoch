from queries import RejectionQuery
from erps import flip
import numpy as np

class ShortTest(RejectionQuery):

    def __init__(self):
        self.a = None
        self.b = None

    def query_model(self):
        self.a = flip()
        if self.a:
            self.b = flip(0.9)
        else:
            self.b = flip(0.4)

    def sample(self):
        return self.a

    def condition(self):
        return self.b

query = ShortTest()
samples = [query.sample() for x in range(100)]

print np.mean(samples)
