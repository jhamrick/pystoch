import pystoch
from pystoch import flip, MetropolisHastings, RejectionQuery

class RejQuery(RejectionQuery):

    def __init__(self):
        self.a = None

    def bit_flip(self, fidelity, x):
        if x:
            return flip(fidelity)
        else:
            return flip(1 - fidelity)

    def query_model(self):
        self.a = flip(0.7)

    def sample(self):
        return self.a

    def condition(self):
        return self.bit_flip(0.8, self.a)

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return RejQuery().run()

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = (0.7*0.8) / (0.7*0.8 + 0.3*0.2)
