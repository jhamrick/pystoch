import pystoch
from pystoch import poisson, MetropolisHastings

TOLERANCE = 0.2
lam = 4

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        global lam
        return poisson(lam)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = lam
