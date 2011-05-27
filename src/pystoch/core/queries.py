"""
pystoch.core.queries
--------------------

"""

import numpy as np

from . import erps
from ..utilities.exceptions import TraceInvalidatedException

def random(func):
    func.random = True
    return func

class RejectionQuery(object):
    global random

    def __init__(self):
        pass

    @random
    def run(self, PYSTOCHOBJ=None):
        test = False
        while (not test):
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.call(self.query_model)
            test = PYSTOCHOBJ.call(self.condition)

        return PYSTOCHOBJ.call(self.sample)

class MetropolisHastings(object):
    global random

    def __init__(self):
        pass

    @random
    def init_rejection_query(self, PYSTOCHOBJ=None):
        self._condition = False
        while not self._condition:
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.call(self.query_model)
            self._condition = PYSTOCHOBJ.call(self.condition)
        self._sample = PYSTOCHOBJ.call(self.sample)

    @random
    def run_query_model(self, PYSTOCHOBJ=None):
        PYSTOCHOBJ.call(self.query_model)
        self._condition = PYSTOCHOBJ.call(self.condition)
        self._sample = PYSTOCHOBJ.call(self.sample)

    @random
    def do_trace_update(self, func, db, PYSTOCHOBJ=None):
        PYSTOCHOBJ.running_query = True
        trace_loglh, db, trace = PYSTOCHOBJ.trace_update(func, db)
        PYSTOCHOBJ.running_query = False
        if not self._condition:
            trace_loglh = -np.inf
        return trace_loglh, db, trace

    @random
    def run(self, num_samples, num_steps, PYSTOCHOBJ=None):
        """Take samples from the MCMC trace sampler.

        Paramters
        ---------
        num_samples : int
            The number of samples to take
        num_steps : int
            The number of traces to accept between taking samples
        PYSTOCHOBJ : pystoch.PyStochObj
            The PYSTOCHOBJ containing the trace state

        """

        num_traces = 0
        num_accepted = 0

        # initialize the database of randomness using a rejection
        # query; this starts off the MCMC from a state that we know is
        # acceptable
        trace_loglh, db, trace = self.do_trace_update(self.init_rejection_query, {}, PYSTOCHOBJ)
        sample = self._sample

        # initialize the list of samples that we will return
        samples = []

        # loop over the number of samples that we want to take
        while num_samples > 0:
            # loop over the number of steps between samples
            steps = num_steps
            while steps > 0:

                # get the number of random variables and the list of
                # random variables used in the last trace
                num_rvs = PYSTOCHOBJ.num_rvs
                rvs = PYSTOCHOBJ.rvs

                rvs.sort()
                #print "rvs: %s" % rvs

                # uniformly select a random choice
                name = rvs[np.random.randint(num_rvs)]
                
                # look up the erp type, the value, and likelihood, the
                # arguments, and the most recent trace that the random
                # choice was used in from the database
                erp, val, erp_loglh, args_db, trace = db[name]

                # propose a new value using the erp's proposal kernel
                new_val = erp.kernel(val, *args_db[0], **args_db[1])

                # calculate the log likelihood for the proposed value
                new_erp_loglh = np.log(erp.prob(
                    new_val, *args_db[0], **args_db[1]))

                # propose a new trace by creating a copy of the
                # current database, updating it with the new value and
                # log likelihood, and then updating the trace
                new_db = db.copy()
                new_db[name] = (erp, new_val, new_erp_loglh, args_db, trace)

                try:
                    new_trace_loglh, new_db, new_trace = self.do_trace_update(
                        self.run_query_model, new_db, PYSTOCHOBJ)

                    # clean out the database of stale values
                    new_db = self.clean_db(new_trace, new_db)

                    forward = self.calc_transition_prob(name, new_db, db)
                    backward = self.calc_transition_prob(name, db, new_db)
                    
                    # score the new trace
                    a = (new_trace_loglh - trace_loglh) + (backward - forward)

                    # print "ERP: %s (%s)" % (name, erp.__name__)
                    # print "Old val:", val
                    # print "New val:", new_val
                    # print "Old erp likelihood", erp_loglh
                    # print "New erp likelihood", new_erp_loglh
                    # print "Old trace likelihood", trace_loglh
                    # print "New trace likelihood", new_trace_loglh
                    # print "Forward", forward
                    # print "Backward", backward
                    # print "a:", a
                    # keys = new_db.keys()
                    # keys.sort()
                    # for key in keys:
                    #     print "%s: %s" % (key, new_db[key])
                    
                except TraceInvalidatedException:
                    # changing the value of the ERP caused the program
                    # to become unrunnable, so reject this trace
                    a = -np.inf
                    
                    # print "trace invalidated"

                num_traces += 1

                # accept the new state
                if np.log(erps._uniform(0, 1)) < a:
                    
                    # set the database, trace number, and trace
                    # likelihood to the ones generated by the new
                    # trace
                    db = new_db
                    trace = new_trace
                    trace_loglh = new_trace_loglh
                    sample = self._sample
                    
                    num_accepted += 1

                    #print 'ACCEPTED'
                    
                else:

                    PYSTOCHOBJ.rvs = rvs
                    PYSTOCHOBJ.num_rvs = num_rvs

                    #print 'REJECTED'
                    
                # update the number of steps we have to go
                steps -= 1

                #print

            # update the number of samples we still have to go, and
            # add the current sample to our list of samples
            num_samples -= 1
            samples.append(sample)

        #if len(samples) > 0:
        #    print "Average acceptance rate: %s%%" % (np.round(float(num_accepted) / num_traces, decimals=4)*100)

        return samples

    def calc_transition_prob(self, erpname, new_db, old_db):
        """
        Calculate the log transition probability from an old state
        (old_db) to a new state (new_db) given the the random variable
        that was changed (erpname).  This probability is composed of
        three parts:

        1) The probability that the random variable was chosen.  When
        a new trace is proposed, a random variable is chosen at random
        from the set of random variables that were last used, so this
        probability is just one over the number of random variables.

        2) The probability that the value for the new random variable
        was chosen given the old value and the parameters.  This is
        calculated from the ERP's kernel.

        3) The probability of any new randomness that was sampled.
        Changing the value of a random variable may cause new
        randomness to be sampled, either by creating new random
        variables or by changing the type of other random variables.

        Parameters
        ----------
        erpname : string
            The name of the ERP that was changed to yield the
            transition.
        new_db : dictionary
            The new database of randomness after the transition.
        old_db : dictionary
            The old database of randomness before the transition.

        """
        
        if erpname not in new_db:
            raise TraceInvalidatedException()

        # lookup the old and new information for the erp
        new_erp, new_val, new_erp_loglh, \
                 new_args_db, new_trace = new_db[erpname]
        old_erp, old_val, old_erp_loglh, \
                 old_args_db, old_trace = old_db[erpname]
        
        # calculate the probability of choosing that RV to flip
        old_numrvs = len(old_db.keys())
        p_choose_rv = np.log(1. / old_numrvs)

        # calculate the probability of choosing that value of the RV
        p_rv_val = np.log(old_erp.kernel.prob(
            new_val, old_val, *old_args_db[0], **old_args_db[1]))

        # calculate the probability of the new randomness that was
        # sampled
        p_randomness = 0
        for rv in new_db:
            # if the random variable wasn't in the old database, then
            # it's new so we can add its log likelihood
            if rv not in old_db:
                p_randomness += new_db[rv][2]
            else:
                new_erp, new_val, new_erp_loglh, \
                         new_args_db, new_trace = new_db[rv]
                old_erp, old_val, old_erp_loglh, \
                         old_args_db, old_trace = old_db[rv]

                # if the type of the random variable changed, then
                # it's also new so we can add its log likelihood
                if new_erp != old_erp:
                    p_randomness += new_erp_loglh

        # and then the transition probability is just the probability
        # of choosing the random variable, the probability of the
        # value of the variable, and the probability of the new
        # randomness
        p_transition = p_choose_rv + p_rv_val + p_randomness
        return p_transition

    def clean_db(self, trace, db):
        for name in db.keys():
            if db[name][4] < trace:
                del db[name]

        return db

    run.random = True
