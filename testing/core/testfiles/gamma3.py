import pystoch
from pystoch import gamma, MetropolisHastings

TOLERANCE = 0.5
k = 9
theta = 0.5

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return gamma(k, theta)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = k * theta
