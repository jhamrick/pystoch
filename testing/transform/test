#!/usr/bin/python

import pystoch
import os
import re
import datetime
import traceback

def to_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) \
           / 10.0**6

# get a list of all of the tests
testfiles = [os.path.join("tests", test) for test in os.listdir("tests") \
             if test.endswith(".py") and not test.startswith(".#")]

# read all of the tests in and stick the code in a dictionary
mytests = {}
for testfile in testfiles:
    back = len(".py")
    name = os.path.basename(testfile)[:-back]
    mytests[name] = testfile

tests.extend(mytests.keys())
print "Tests: %s" % ", ".join(mytests.keys())
print

testkeys = mytests.keys()
testkeys.sort()
for testname in testkeys:

    test = mytests[testname]
    testfailed = False

    # test the python code
    before = datetime.datetime.now()
    try:
        execfile(test)
        pythonlocals = locals()
        pythonresult = pythonlocals['result']
    except:
        pythonresult = traceback.format_exc()
        testfailed = True
    after = datetime.datetime.now()
    pythontime = to_seconds(after-before)

    # run the python code as pystoch code
    before = datetime.datetime.now()
    try:
        pystochlocals = pystoch.run(test)
        pystochresult = pystochlocals['result']
    except:
        pystochresult = traceback.format_exc()
        testfailed = True
    after = datetime.datetime.now()
    pystochtime = to_seconds(after-before)

    testfailed = testfailed or (pythonresult != pystochresult)
    print_results(testname, pythonresult, pythontime,
                  pystochresult, pystochtime, testfailed)

    if testfailed:
        failed.append(testname)
    else:
        passed.append(testname)

    print
