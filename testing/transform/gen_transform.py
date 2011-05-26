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

    gen = open('transform.py', 'w')
    gen.write("""import pystoch
import unittest
import sys

class TestTransform(unittest.TestCase):

    def _run_test(self, filename):
        pythonlocals = {}
        execfile(filename, pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run(filename)
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

""")
    
    for testfile in testfiles:
        back = len('.py')
        name = 'test_' + os.path.basename(testfile)[:-back]
        
        gen.write("""    def %s(self):
        self._run_test('%s')

""" % (name, testfile  ))

    gen.write('''if __name__ == "__main__":
    testlist = unittest.TestSuite()
    if len(sys.argv) > 1:
        for test in sys.argv[1:]:
            testlist.addTest(TestTransform('test_' + test))
    else:
        testlist.addTest(unittest.makeSuite(TestTransform))
    result = unittest.TextTestRunner(verbosity=2).run(testlist)
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)
    ''')

    gen.close()
    
if len(sys.argv) > 1:
    gentests(sys.argv[1])
else:
    gentests()
