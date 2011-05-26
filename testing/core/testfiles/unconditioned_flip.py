import pystoch
from pystoch import flip, MetropolisHastings

class UnconditionedFlip(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return flip(0.7)

    def condition(self):
        return True

query = UnconditionedFlip()
result = query.run(SAMPLES, LAG)
exresult = 0.7
