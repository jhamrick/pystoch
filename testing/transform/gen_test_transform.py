import os
import pystoch
import unittest
import sys

def gentests(dir="testfiles"):
    # get a list of all of the tests
    testfiles = [os.path.join(dir, test) for test \
                 in os.listdir(dir) \
                 if test.endswith(".py") and \
                 not test.startswith(".#")]
    testfiles.sort()

    if len(testfiles) == 0:
        print "No test files, exiting."
        sys.exit(0)

    gen = open('test_transform.py', 'w')
    gen.write('''import pystoch
import unittest
import sys

class TestTransform(unittest.TestCase):

''')
    
    for testfile in testfiles:
        back = len('.py')
        name = 'test_' + os.path.basename(testfile)[:-back]
        
        gen.write("""    def %s(self):
        pythonlocals = {}
        execfile('%s', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('%s')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

""" % (name, testfile, testfile))

    gen.write('''if __name__ == "__main__":
    testlist = unittest.TestSuite()
    testlist.addTest(unittest.makeSuite(TestTransform))
    result = unittest.TextTestRunner(verbosity=2).run(testlist)
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)
    ''')

    gen.close()
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        gentests(sys.argv[1])
    else:
        gentests()
