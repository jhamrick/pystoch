import pystoch
from pystoch import beta, MetropolisHastings

a = 5
b = 1

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        global a, b
        return beta(a, b)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = a / float(a + b)
