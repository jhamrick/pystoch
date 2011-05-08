class RejectionQuery(object):
    random = True

    def __init__(self, PYSTOCHOBJ=None):
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_47e6cad0')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()
        return 
    __init__.random = True

    def run(self, PYSTOCHOBJ=None):
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
    run.random = True

class MetropolisHastings(object):
    random = True

    def __init__(self, PYSTOCHOBJ=None):
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_63f57499')
        PYSTOCHOBJ.line_stack.push(0)
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()
        return 
    __init__.random = True

    def run(self, PYSTOCHOBJ=None):
        PYSTOCHOBJ.func_stack.push('PYSTOCHID_865eb7e4')
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
        PYSTOCHID_3af23191 = PYSTOCHOBJ.call(self.sample)
        PYSTOCHOBJ.line_stack.pop()
        PYSTOCHOBJ.func_stack.pop()
        return PYSTOCHID_3af23191
    run.random = True
