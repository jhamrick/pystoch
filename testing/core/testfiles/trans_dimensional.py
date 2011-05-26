import pystoch
from pystoch import flip, beta, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.a = None
        self.b = None

    def query_model(self):
        if flip(0.9):
            self.a = beta(1, 5)
        else:
            self.a = 0.7

        self.b = flip(self.a)

    def sample(self):
        return self.a

    def condition(self):
        return self.b

result = Query().run(SAMPLES, LAG)
exresult = 0.417
