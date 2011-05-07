class RejectionQuery(object):

    def __init__(self, PYSTOCHOBJ=None):
        pass
    __init__.random = True

    def run(self, PYSTOCHOBJ=None):
        self.query_model(PYSTOCHOBJ=PYSTOCHOBJ)
        while not self.condition(PYSTOCHOBJ=PYSTOCHOBJ):
            self.query_model(PYSTOCHOBJ=PYSTOCHOBJ)

        return self.sample(PYSTOCHOBJ=PYSTOCHOBJ)
    run.random = True
