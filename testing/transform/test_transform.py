import pystoch
import unittest
import sys

class TestTransform(unittest.TestCase):

    def test_bottles_of_beer(self):
        pythonlocals = {}
        execfile('testfiles/bottles_of_beer.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/bottles_of_beer.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_classes(self):
        pythonlocals = {}
        execfile('testfiles/classes.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/classes.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_conditionals(self):
        pythonlocals = {}
        execfile('testfiles/conditionals.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/conditionals.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_eight_queens(self):
        pythonlocals = {}
        execfile('testfiles/eight_queens.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/eight_queens.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_enumerate(self):
        pythonlocals = {}
        execfile('testfiles/enumerate.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/enumerate.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_fibonacci(self):
        pythonlocals = {}
        execfile('testfiles/fibonacci.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/fibonacci.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_function1(self):
        pythonlocals = {}
        execfile('testfiles/function1.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/function1.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_function2(self):
        pythonlocals = {}
        execfile('testfiles/function2.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/function2.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_function_composition1(self):
        pythonlocals = {}
        execfile('testfiles/function_composition1.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/function_composition1.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_function_composition2(self):
        pythonlocals = {}
        execfile('testfiles/function_composition2.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/function_composition2.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_functions(self):
        pythonlocals = {}
        execfile('testfiles/functions.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/functions.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_generators(self):
        pythonlocals = {}
        execfile('testfiles/generators.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/generators.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_itertools(self):
        pythonlocals = {}
        execfile('testfiles/itertools.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/itertools.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_list_comprehension(self):
        pythonlocals = {}
        execfile('testfiles/list_comprehension.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/list_comprehension.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_mapreduce(self):
        pythonlocals = {}
        execfile('testfiles/mapreduce.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/mapreduce.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_output(self):
        pythonlocals = {}
        execfile('testfiles/output.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/output.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_primes(self):
        pythonlocals = {}
        execfile('testfiles/primes.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/primes.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_regular_expressions(self):
        pythonlocals = {}
        execfile('testfiles/regular_expressions.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/regular_expressions.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_stocks(self):
        pythonlocals = {}
        execfile('testfiles/stocks.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/stocks.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

    def test_xml_parsing(self):
        pythonlocals = {}
        execfile('testfiles/xml_parsing.py', pythonlocals)
        pythonresult = pythonlocals['result']

        pystochlocals = pystoch.run('testfiles/xml_parsing.py')
        pystochresult = pystochlocals['result']

        assert pythonresult == pystochresult

if __name__ == "__main__":
    testlist = unittest.TestSuite()
    testlist.addTest(unittest.makeSuite(TestTransform))
    result = unittest.TextTestRunner(verbosity=2).run(testlist)
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)
    