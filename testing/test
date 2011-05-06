import pystoch
import pystoch.compile as c
import os
import re

testfiles = [os.path.join("tests", test) for test in os.listdir("tests") \
             if test.endswith(".py") and test.startswith("compile_")]
resultfiles = [os.path.join("tests", test) for test in os.listdir("tests") \
               if test.endswith(".pystoch") and test.startswith("compile_")]

tests = {}
for testfile in testfiles:
    front = len("compile_")
    back = len(".py")
    name = os.path.basename(testfile)[front:-back]
    tests[name] = open(testfile, "r").read()

results = {}
for resultfile in resultfiles:
    front = len("compile_")
    back = len(".pystoch")
    name = os.path.basename(resultfile)[front:-back]
    results[name] = open(resultfile, "r").read()

teststorun = list(set(tests.keys()).intersection(set(results.keys())))
print "Tests: %s" % ", ".join(teststorun)
print

passed = []
failed = []
for totest in teststorun:
    print "-----------------------------------------------"
    print "*** Running '%s' test... ***" % totest
    print "-----------------------------------------------"

    test = tests[totest]
    result = re.sub(r'PYSTOCHID_[a-z0-9]{8}', 
                    r'PYSTOCHID',
                    c.pystoch_compile(tests[totest]))
    exresult = results[totest]

    def indent(src):
        return "\n".join(["\t" + line for line in src.split("\n")])
        
    print "TEST"
    print indent(test)
    print "RESULT"
    print indent(result)
    print "EXPECTED RESULT"
    print indent(exresult)
        
    if result != exresult:
        print "FAILED"
        failed.append(totest)
    else:
        print "PASSED"
        passed.append(totest)

    print

print "-----------------------------------------------"
print
print "Tests passed: %s/%s" % (len(passed), len(teststorun))
print "Tests failed: %s/%s" % (len(failed), len(teststorun))
print
print "Failed tests: %s" % ", ".join(failed)
