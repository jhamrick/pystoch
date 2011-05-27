import pystoch
from pystoch import binomial, MetropolisHastings

TOLERANCE = 0.2

n = 10
p = 0.2

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        global n, p
        return binomial(n, p)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = n * p
