from queries import MetropolisHastings
from erps import flip
import numpy as np

class ShortTest(MetropolisHastings):

    def __init__(self):
        self.a = None
        self.b = None

    def query_model(self):
        self.a = flip(0.5)
        if self.a:
            self.b = flip(0.9)
        else:
            self.b = flip(0.4)

    def sample(self):
        return self.a

    def condition(self):
        return self.b

query = ShortTest()
samples = query.run(100, 100)

print samples
print np.mean(samples)
