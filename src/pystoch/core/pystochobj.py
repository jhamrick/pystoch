"""
pystoch.core.pystochobj
-----------------------

"""

from ..utilities.stack import Stack
from ..utilities.exceptions import TraceInvalidatedException

import numpy as np

class PyStochObj(object):
    """pystoch.PyStochObj

    This class maintains the state of a trace of a PyStoch program.
    It keeps track of the current stack trace (using function, line,
    and loop stacks), as well as keeping a database of random choices,
    which stores the type, value, log likelihood, parameters and trace
    number.  Additionally, the PyStochObj keeps track of the number of
    random variables encountered, as well as their names.

    Member Variables
    ----------------
    self.func_stack : Stack
        The function stack. Used for naming random choices.
    self.line_stack : Stack
        The line stack. Used for naming random choices.
    self.loop_stack : Stack
        The loop stack.  Used for naming random choices

    self.db : dictionary
        The database of randomness
    self.curr_trace : integer
        The number of the current trace

    self.num_rvs : integer
        The number of random variables encountered so far in the
        current trace
    self.rvs : list of strings
        The names of the random variables encountered so far in the
        current trace
    self.trace_loglh : float
        The log likelihood so far of the current trace

    Methods
    -------

    call(self, func, *args, **kwargs)
        Call a function
        
    print_trace(self)
        Print the current stack trace

    trace_update(self, func, db)
        Run a new trace of func using the specified database
        
    update_db(self, erp_curr, args_curr)
        Update the database of randomness with the current ERP

    clear(self)
        Clear the number of random variables, the list of random
        variables, and the trace log likelihood

    """

    def __init__(self):
        """Initialize a PyStochObject.

        This initializes the function, line, and loop stacks.  It also
        creates a new database, sets the current trace number to zero,
        and initializes the number of random variables, the list of
        random variables, and the total trace log likelihood to None.

        """
        
        self.func_stack = Stack()
        self.line_stack = Stack()
        self.loop_stack = Stack()

        self.db = {}
        self.curr_trace = 0

        self.num_rvs     = None
        self.rvs         = None
        self.trace_loglh = None
            
    def call(self, func, *args, **kwargs):
        """Call a function.

        If the function is random (has the random attribute set to
        True), then call the function with *args and **kwargs,
        additionally adding a PYSTOCHOBJ=self kwarg.

        If the function is an ERP (has the erp attribute set to True),
        then pass the function and its arguments to update_db.

        Otherwise, just call the function as normal.

        Parameters
        ----------
        func : function
            The function to call
        args : tuple of arguments
            The arguments to be passed to the function
        kwargs : dictionary of keyword arguments
            The keyword arguments to be passed to the function

        Returns
        -------
        out : variable
           The value of calling func(*args, **kwargs)

        """
        
        if hasattr(func, "random") and func.random:
            kwargs['PYSTOCHOBJ'] = self

        if hasattr(func, "erp") and func.erp:
            return self.update_db(func, (args, kwargs))

        return func(*args, **kwargs)
            
    def print_trace(self):
        """Print the current stack trace, that is, the current values
        of the function, line, and loop stacks.

        """
        
        print "Func:  ", str(self.func_stack)
        print "Line:  ", str(self.line_stack)
        print "Loop:  ", str(self.loop_stack)

    def trace_update(self, func, db):
        """Perform a new trace of `func`, using `db` as the new database of randomness.

        Parameters
        ----------
        func : function
            The function to perform the trace on
        db : dictionary
            The new database of randomness

        Returns
        -------
        out : three-tuple
            (trace log likelihood, updated database, current trace number)

        """

        # clear the old trace values and update the database with the
        # one passed in
        self.clear_trace()
        self.db = db

        # run the trace on the function and update the current trace
        # number
        self.call(func)
        self.curr_trace += 1
        
        return self.trace_loglh, self.db, self.curr_trace-1

    def update_db(self, erp_curr, args_curr):
        """Update the database with the current random choice.

        If the choice already exists in the database via its name
        (determined by stack traces), and its parameters match the
        parameters stored in the database, then we can just reuse the
        old value.  If the parameters don't match, then we recompute
        the likelihood of the stored value.  If the value isn't found
        in the database at all, then we sample a new value and
        calculate its likelihood.  Finally, we update the database
        with the new value and likelihood, if necessary.

        Paramters
        ---------
        erp_curr : function with erp attribute set to True
            The random choice to update the database with
        args_curr : tuple
            A two-tuple, with the first element being the arguments to
            pass to erp_curr and the second element being the keyword
            arguments to pass to erp_curr

        Returns
        -------
        out : number
            The value of calling erp_curr(*args_curr[0], **args_curr[1])

        """
        
        # calculate the name of the current random choice
        name = "%s-%s-%s" % (self.func_stack.peek(),
                             self.line_stack.peek(),
                             self.loop_stack.peek())

        # look up the name in the database
        if name in self.db:
            erp_db, val, erp_loglh, args_db, trace = self.db[name]
            success = True
        else:
            success = False

        # if the random choice was found in the database and the ERP
        # type matches that found in the database
        if success and erp_curr == erp_db:

            # if the args that the current random choice was called
            # with are not the same as those stored in the database
            if args_curr != args_db:
                
                # rescore the log likelihood by drawing from the
                # probability density/mass function for the ERP
                erp_loglh = np.log(erp_curr.prob(val, *args_curr[0], **args_curr[1]))
                if erp_loglh == -np.inf:
                    raise TraceInvalidatedException()

        # if the erp type changed, then we need to resample
        else:
            # sample a new value from the distribution and calculate
            # its log likelihood
            val = erp_curr(*args_curr[0], **args_curr[1])
            erp_loglh = np.log(erp_curr.prob(val, *args_curr[0], **args_curr[1]))
            

        # update the database to reflect any changes (including that
        # this random choice was used during this trace)
        self.db[name] = (erp_curr, val, erp_loglh, args_curr, self.curr_trace)
        # update the total log likelihood of the trace
        self.trace_loglh += erp_loglh

        # update the total number of random variables encountered
        # during this trace
        self.num_rvs += 1
        # add the name of the random choice to the list of all random
        # choices in this trace
        self.rvs.append(name)

        # return the value of the random choice
        return val

    def clear_trace(self):
        """Clear the current trace values.  This involves setting the
        trace log likelihood to zero, the number of random variables
        to zero, and the list of random variables to an empty list.

        """
        
        self.trace_loglh = 0
        self.num_rvs = 0
        self.rvs = []
