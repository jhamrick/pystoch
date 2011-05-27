import pystoch
from pystoch import uniform, MetropolisHastings

low = -1.0
high = 1.0

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        return uniform(low, high)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = (low + high) / 2.0
