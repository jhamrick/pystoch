import pystoch
from pystoch import flip, MetropolisHastings

class Query(MetropolisHastings):

    def __init__(self):
        self.proc = None
        self.samp = None

    def proc1(self, x):
        return flip(0.2)

    def proc2(self, x):
        return flip(0.8)

    def query_model(self):
        if flip(0.7):
            self.proc = self.proc1
        else:
            self.proc = self.proc2

        self.samp = self.proc(1)

    def sample(self):
        return self.samp

    def condition(self):
        return True

result = Query().run(SAMPLES, LAG)
exresult = 0.7*0.2 + 0.3*0.8
