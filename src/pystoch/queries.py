class RejectionQuery(object):

    def __init__(self):
        pass

    def run(self):
        self.query_model()
        while not self.condition():
            self.query_model()

        return self.sample()

        
