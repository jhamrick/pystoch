import os
import pystoch
import unittest
import sys

def gentests(dir="testfiles"):
    # get a list of all of the tests
    testfiles = [os.path.join(os.getcwd(), dir, test) for test \
                 in os.listdir(dir) \
                 if test.endswith(".py") and \
                 not test.startswith(".#")]
    testfiles.sort()

    if len(testfiles) == 0:
        print "No test files, exiting."
        sys.exit(0)

    gen = open('core.py', 'w')
    gen.write("""import pystoch
import unittest
import sys
import numpy as np

RUNS = 1

class TestCore(unittest.TestCase):

    def _run_test(self, filename):
        global RUNS
        
        results = []
        exresults = []
        for i in xrange(RUNS):
            localsdict = {
                'SAMPLES' : 300,
                'LAG' : 20,
                'TOLERANCE' : 0.07
            }
            pystochlocals = pystoch.run(filename, localsdict=localsdict)
            result = pystochlocals['result']
            exresult = pystochlocals['exresult']
            tolerance = pystochlocals['TOLERANCE']
            results.append(result)
            exresults.append(exresult)

        estimates = []
        errors = []
        for result, exresult in zip(results, exresults):
            estimate = np.mean(result)
            error = np.abs(estimate - exresult)
            estimates.append(estimate)
            errors.append(error)

        mean_abs_error = np.round(np.mean(errors), decimals=5)
        std_error = np.std(errors)

        assert mean_abs_error <= tolerance, \\
               'true expectation: %s, test mean: %s' % \\
               (exresult, np.mean(estimates))

""")
    
    for testfile in testfiles:
        back = len('.py')
        name = 'test_' + os.path.basename(testfile)[:-back]
        
        gen.write("""    def %s(self):
        self._run_test('%s')

""" % (name, testfile  ))

    gen.write("""if __name__ == '__main__':
    testlist = unittest.TestSuite()
    if len(sys.argv) > 1:
        for test in sys.argv[1:]:
            testlist.addTest(TestCore('test_' + test))
    else:
        testlist.addTest(unittest.makeSuite(TestCore))
    result = unittest.TextTestRunner(verbosity=2).run(testlist)
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)
    """)

    gen.close()
    
if len(sys.argv) > 1:
    gentests(sys.argv[1])
else:
    gentests()
