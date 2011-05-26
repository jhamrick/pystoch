import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.val = None

    def query_model(self):
        if flip(0.7):
            self.val = flip(0.2)
        else:
            self.val = flip(0.8)

    def sample(self):
        return self.val
        
    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0.7*0.2 + 0.3*0.8
