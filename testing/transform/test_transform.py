import datetime
import os
import pystoch
import re
import traceback
import unittest

class TestTransform(unittest.TestCase):

    def setUp(self):
        # get a list of all of the tests
        testfiles = [os.path.join("tests", test) for test \
                     in os.listdir("tests") \
                     if test.endswith(".py") and \
                     not test.startswith(".#")]
        testfiles.sort()

        def gentest(test):
            def mytest(self):
                # test the python code
                try:
                    execfile(test)
                    pythonlocals = locals()
                    pythonresult = pythonlocals['result']
                except:
                    pythonresult = traceback.format_exc()
                    testfailed = True

                # run the python code as pystoch code
                try:
                    pystochlocals = pystoch.run(test)
                    pystochresult = pystochlocals['result']
                except:
                    pystochresult = traceback.format_exc()
                    testfailed = True

        for testfile in testfiles:
            back = len(".py")
            name = os.path.basename(testfile)[:-back]
            setattr(self, "test_%s" % name, gentest(name))
        

        # read all of the tests in and stick the code in a dictionary
        tests = {}
        for testfile in testfiles:
            tests[name] = testfile


    testfailed = testfailed or (pythonresult != pystochresult)
    print_results(testname, pythonresult, pythontime,
                  pystochresult, pystochtime, testfailed)

    if testfailed:
        failed.append(testname)
    else:
        passed.append(testname)

    print
