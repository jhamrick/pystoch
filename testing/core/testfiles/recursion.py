import pystoch
from pystoch import flip, MetropolisHastings, hist

thresh = 5

class Query(MetropolisHastings):

    def __init__(self):
        self.a = None

    def power_law(self, prob, x):
        if flip(prob):
            return x
        else:
            return self.power_law(prob, x + 1)

    def query_model(self):
        self.a = self.power_law(0.3, 1)

    def sample(self):
        global thresh
        return self.a < thresh

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0

prob = 0.3
for x in xrange(1, thresh):
    exresult += ((1 - prob) ** (x - 1)) * prob
