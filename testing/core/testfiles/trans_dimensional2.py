import pystoch
from pystoch import flip, exponential, gaussian,\
     MetropolisHastings, truehist

class Query(MetropolisHastings):

    def __init__(self):
        self.a = None
        self.b = None

    def query_model(self):
        if flip(0.9):
            self.a = exponential(2.0)
        else:
            self.a = 0.7

        self.b = gaussian(self.a, 1.0)

    def sample(self):
        return self.a

    def condition(self):
        return self.b > 0.7

result = Query().run(SAMPLES, LAG)
exresult = 0.699
