import pystoch
from pystoch import flip, MetropolisHastings

TOLERANCE = 0.0

class SetFlip(MetropolisHastings):

    def __init__(self):
        self.a = None

    def query_model(self):
        self.a = 1. / 1000

    def condition(self):
        return flip(self.a)
        
    def sample(self):
        return self.a

query = SetFlip()
result = query.run(SAMPLES, LAG)
exresult = 1. / 1000
