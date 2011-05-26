import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        pass

    def query_model(self):
        pass

    def sample(self):
        if flip(0.7):
            weight = 0.2
        else:
            weight = 0.8
        return flip(weight)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0.7*0.2 + 0.3*0.8
