import erps
import numpy as np

def random(func):
    func.random = True
    return func

class RejectionQuery(object):
    global random

    def __init__(self):
        pass

    @random
    def run(self, PYSTOCHOBJ=None):
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_ad8a8f0c')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.set(1)
        test = False
        PYSTOCHOBJ.line_stack.set(2)
        PYSTOCHOBJ.loop_stack.push(0)
        while (not test):
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.loop_stack.increment()
            PYSTOCHOBJ.line_stack.set(3)
            PYSTOCHOBJ.call(self.query_model)
            PYSTOCHOBJ.line_stack.set(4)
            test = PYSTOCHOBJ.call(self.condition)
        PYSTOCHOBJ.loop_stack.pop()
        PYSTOCHOBJ.line_stack.set(5)
        PYSTOCHID_e9cd7cea = PYSTOCHOBJ.call(self.sample)
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()
        return PYSTOCHID_e9cd7cea

class MetropolisHastings(object):
    global random

    def __init__(self):
        pass

    def kernel(self, erp, val, args):
        return erp(*args[0], **args[1])
    def _kernel_pdf(erp, new_val, val, args):
        return erp.prob(new_val, *args[0], **args[1])
    kernel.pdf = _kernel_pdf

    @random
    def init_rejection_query(self, PYSTOCHOBJ):
        PYSTOCHOBJ.clear_trace()
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_7192ffd0')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.set(1)
        test = False
        PYSTOCHOBJ.line_stack.set(2)
        PYSTOCHOBJ.loop_stack.push(0)
        while (not test):
            PYSTOCHOBJ.clear_trace()
            PYSTOCHOBJ.db = {}
            PYSTOCHOBJ.loop_stack.increment()
            PYSTOCHOBJ.line_stack.set(3)
            PYSTOCHOBJ.call(self.query_model)
            PYSTOCHOBJ.line_stack.set(4)
            test = PYSTOCHOBJ.call(self.condition)
        PYSTOCHOBJ.loop_stack.pop()
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()

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

        # initialize the database of randomness using a rejection
        # query; this starts off the MCMC from a state that we know is
        # acceptable
        trace_loglh, db, trace = PYSTOCHOBJ.trace_update(self.init_rejection_query, {})

        # initialize the list of samples that we will return
        samples = []

        # loop over the number of samples that we want to take
        while num_samples > 0:
            # loop over the number of steps between samples
            steps = num_steps
            while steps > 0:
                # get the number of random variables and the list of
                # random variables used in the last trac
                num_rvs = PYSTOCHOBJ.num_rvs
                rvs = PYSTOCHOBJ.rvs

                # uniformly select a random choice
                name = rvs[np.random.randint(num_rvs)]
                
                # look up the erp type, the value, and likelihood, the
                # arguments, and the most recent trace that the random
                # choice was used in from the database
                erp, val, erp_loglh, args_db, trace = db[name]

                # propose a new value using the erp's proposal kernel
                # TODO: am I doing this right?
                new_val = self.kernel(erp, val, args_db)

                print "ERP: %s" % name
                print "Old value: %s" % val
                print "New value: %s" % new_val

                # using the proposed value, calculate the forward and
                # backward probability, as well as the log likelihood
                # for that probability
                forward = np.log(self.kernel.pdf(erp, new_val, val, args_db))
                backward = np.log(self.kernel.pdf(erp, val, new_val, args_db))
                new_erp_loglh = np.log(erp.prob(new_val, *args_db[0], **args_db[1]))

                # propose a new trace by creating a copy of the
                # current database, updating it with the new value and
                # log likelihood, and then updating the trace
                new_db = db
                assert new_db == db
                new_db[name] = (erp, new_val, new_erp_loglh, args_db, trace)
                new_trace_loglh, new_db, new_trace = PYSTOCHOBJ.trace_update(self.query_model, new_db)
                assert new_db != db
                
                # score the new trace
                a = new_trace_loglh - trace_loglh + backward - forward

                # accept the new state
                if np.log(erps.uniform(0, 1)) < a:

                    # set the database, trace number, and trace
                    # likelihood to the ones generated by the new
                    # trace
                    db = new_db
                    trace = new_trace
                    trace_loglh = new_trace_loglh

                    # clean out the database of stale values
                    self.clean_db(trace, db)

                    # update the number of steps we have to go
                    steps -= 1

            # update the number of samples we still have to go, and
            # add the current sample to our list of samples
            num_samples -= 1
            samples.append(PYSTOCHOBJ.call(self.sample))

        return samples

    def clean_db(self, trace, db):
        for name in db.keys():
            if db[name][4] < trace - 1:
                del db[name]

    run.random = True
