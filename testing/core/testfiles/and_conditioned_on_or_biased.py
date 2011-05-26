import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.a = None
        self.b = None

    def query_model(self):
        self.a = flip(0.3)
        self.b = flip(0.3)

    def sample(self):
        return int(self.a and self.b)

    def condition(self):
        return self.a or self.b

query = Query()
result = query.run(SAMPLES, LAG)
exresult = (0.3*0.3) / (0.3*0.3 + 0.3*0.7 + 0.3*0.7)
