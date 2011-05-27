import pystoch
from pystoch import exponential, MetropolisHastings

TOLERANCE = 0.1
lam = 1.5

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        global lam
        return exponential(lam)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 1. / lam
