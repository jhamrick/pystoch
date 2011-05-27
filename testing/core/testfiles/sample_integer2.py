import pystoch
from pystoch import sample_integer, MetropolisHastings

TOLERANCE = 1.0
low = -8
high = 2

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return sample_integer(low, high)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = (low + high) / 2.
