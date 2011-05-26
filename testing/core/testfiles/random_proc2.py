import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.proc = None

    def proc1(self, x):
        return flip(0.2)

    def proc2(self, x):
        return flip(0.8)

    def query_model(self):
        if flip(0.7):
            self.proc = self.proc1
        else:
            self.proc = self.proc2

    def sample(self):
        return self.proc(1)

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0.7*0.2 + 0.3*0.8
