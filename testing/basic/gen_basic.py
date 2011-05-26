import shutil
import subprocess as sp

sp.call(['pytg', '-m', 'pystoch', '-o', 'all', '-g'])
shutil.move('pytestgen_pystoch.py', 'basic.py')
basic = open('basic.py', 'r')
contents = basic.read()
basic.close()

basic = open('basic.py', 'w')
contents = contents.replace('PyUnitframework', 'TestBasic')
basic.write(contents)
