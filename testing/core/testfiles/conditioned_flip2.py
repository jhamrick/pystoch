import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.hyp = None

    def bit_flip(self, fidelity, x):
        if x:
            return flip(fidelity)
        else:
            return flip(1 - fidelity)

    def query_model(self):
        self.hyp = flip(0.7)
        
    def sample(self):
        return self.hyp

    def condition(self):
        return self.bit_flip(0.8, self.hyp)

query = Query()
result = query.run(SAMPLES, LAG)
exresult = (0.7*0.8) / (0.7*0.8 + 0.3*0.2)
