import pystoch
from pystoch.queries import MetropolisHastings, RejectionQuery
from pystoch.erps import flip, uniform_draw
from pystoch.graphing import line_plot

import numpy as np
import datetime
import random
import matplotlib.pyplot as plt

# (define (samples data) 
#    (mh-query
#     100 10

#     (define (hypothesis->set  hyp)
#       (if (equal? hyp  'Big) '(a b c d e f) '(a b c)))
    
#     (define hypothesis (if (flip) 'Big 'Small))
#     (define (observe N) 
#       (repeat N (lambda () (uniform-draw (hypothesis->set hypothesis)))))
    
#     hypothesis
    
#     (equal? (observe (length data)) data)
#     )
#    )

# (define (big-freq data) (mean (map (lambda (hyp) (if (equal? hyp 'Big) 1.0 0.0)) (samples data))))

# (lineplot-value (pair 1 (big-freq '(a))) "Prob. of hypothesis Big")
# (lineplot-value (pair 3 (big-freq '(a b a))) "Prob. of hypothesis Big")
# (lineplot-value (pair 5 (big-freq '(a b a b b))) "Prob. of hypothesis Big")
# (lineplot-value (pair 7 (big-freq '(a b a b b a b))) "Prob. of hypothesis Big")

BIG = 1.0
SMALL = 0.0

class Test(MetropolisHastings):

    global BIG, SMALL

    def __init__(self, data):
        self.data = data[:]
        self.data.sort()

    def hypothesis_set(self, hyp):
        if hyp == BIG:
            return ["a", "b", "c", "d", "e", "f"]
        return ["a", "b", "c"]

    def query_model(self):
        if flip():
            self.hypothesis = BIG
        else:
            self.hypothesis = SMALL

        self.observations = [uniform_draw(self.hypothesis_set(self.hypothesis)) for i in xrange(len(self.data))]
        self.observations.sort()

    def sample(self):
        return self.hypothesis

    def condition(self):
        return self.observations == self.data

num_samples = 1000
num_steps = 10
x = np.arange(1, 8, 2)
y = np.zeros([4])

data = ["a", "b", "a", "b", "b", "a", "b"]
for i in xrange(1, 8, 2):
    print i, data[:i]
    query = Test(data[:i])
    samples = query.run(num_samples, num_steps)
    y[(i-1)/2] = np.mean(samples)

print x
print y
line_plot(x, y, "Probability of Hypothesis Big", path="../../../graphs/test5.pdf")
