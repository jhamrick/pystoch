class RejectionQuery(object):

    def __init__(self):
        pass

    def run(self):
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_882956cd')
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
        PYSTOCHID_952de0a1 = PYSTOCHOBJ.call(self.sample)
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()
        return PYSTOCHID_952de0a1

class MetropolisHastings(object):

    def __init__(self, samples, steps):
        self.samples = samples
        self.steps = steps

    def kernel(val, args):
        return 0.0

    def run(self, PYSTOCHOBJ=None):
        trace_lh, db = PYSTOCHOBJ.trace_update(self.query_model, {})

        while True:
            # TODO: pick random R.V. via name
            name = None
            erp, val, erp_lh, args_db = db[name]
            # TODO: propose new value
            new_val = self.kernel(val, args)
            F = np.log(self.kernel())
            R = np.log(self.kernel())
            new_erp_lh = np.log(dist())

            new_db = db
            new_db[name] = (erp, new_val, new_erp_lh, args_db)
            new_trace_lh, new_db = PYSTOCHOBJ.trace_update(self.query_model, new_db)
            if np.log(rand) < new_trace_lh - trace_lh + R - F:
                # accept
                db = new_db
                trace_lh = new_trace_lh
                # clean out unused values from db
            else:
                # reject, discard db
                pass
            
    run.random = True
