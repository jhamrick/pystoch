#!/usr/bin/python

from pystochobj import PyStochObj

import argparse
import compile as c
import os
import sys
import tempfile

def run(prog, args):
    PYSTOCHOBJ = PyStochObj()

    filename = None
    tempname = None
    sys.argv = [prog] + args
    
    if prog.endswith('.pystoch'):
        filename = prog
    else:
        source = c.pystoch_compile(prog)
        temp = tempfile.NamedTemporaryFile(
            prefix='tmp_', suffix='.pystoch', dir='/tmp', delete=False)
        temp.write(source)
        temp.close()
        filename = temp.name
        tempname = temp.name

    try:
        execfile(filename, {'PYSTOCHOBJ': PYSTOCHOBJ, 'sys': sys})
    finally:
        if tempname is not None:
            os.remove(temp.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a PyStoch program.')
    parser.add_argument('program', metavar='file', type=str, nargs=1,
                        help='the PyStoch file to execute')
    parser.add_argument('arguments', metavar='arg', type=str, nargs='*',
                        help='arguments to the PyStoch program')

    args = parser.parse_args()
    run(args.program[0], args.arguments)
    
