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
        PYSTOCHOBJ.clear()
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_ad8a8f0c')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.set(1)
        test = False
        PYSTOCHOBJ.line_stack.set(2)
        PYSTOCHOBJ.loop_stack.push(0)
        while (not test):
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
        return erp(*args)
    def _kernel_pdf(erp, new_val, val, args):
        return erp.prob(new_val, *args)
    kernel.pdf = _kernel_pdf

    @random
    def init_rejection_query(self, PYSTOCHOBJ):
        PYSTOCHOBJ.clear()
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_7192ffd0')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.set(1)
        test = False
        PYSTOCHOBJ.line_stack.set(2)
        PYSTOCHOBJ.loop_stack.push(0)
        while (not test):
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
        trace_lh, db, trace = PYSTOCHOBJ.trace_update(self.init_rejection_query, {})
        samples = []

        while num_samples > 0:
            steps = num_steps
            while steps > 0:
                num_rvs = PYSTOCHOBJ.num_rvs
                rvs = PYSTOCHOBJ.rvs
                name = rvs[np.random.randint(num_rvs)]
                erp, val, erp_lh, args_db, trace = db[name]

                # propose a new value
                new_val = self.kernel(erp, val, args_db)
                forward = np.log(self.kernel.pdf(erp, new_val, val, args_db))
                backward = np.log(self.kernel.pdf(erp, val, new_val, args_db))
                new_erp_lh = np.log(erp.prob(new_val, *args_db))

                # propose new trace
                new_db = db
                new_db[name] = (erp, new_val, new_erp_lh, args_db, trace)
                new_trace_lh, new_db, new_trace = PYSTOCHOBJ.trace_update(self.query_model, new_db)
                
                # score the trace
                a = new_trace_lh - trace_lh + backward - forward

                # accept the new state
                if np.log(erps.uniform(0, 1)) < a:
                    db = new_db
                    trace = new_trace
                    trace_lh = new_trace_lh
                    self.clean_db(trace, db)
                    steps -= 1

            num_samples -= 1
            samples.append(PYSTOCHOBJ.call(self.sample))

        return samples

    def clean_db(self, trace, db):
        for name in db.keys():
            if db[name][4] < trace:
                del db[name]

    run.random = True
