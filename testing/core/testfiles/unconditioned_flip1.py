import pystoch
from pystoch import flip, MetropolisHastings

class UnconditionedFlip(MetropolisHastings):

    def __init__(self):
        self.val = None

    def query_model(self):
        self.val = int(flip(0.7))

    def sample(self):
        return self.val

    def condition(self):
        return True

query = UnconditionedFlip()
result = query.run(SAMPLES, LAG)
exresult = 0.7
