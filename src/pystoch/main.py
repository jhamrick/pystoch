#!/usr/bin/python

from pystoch import PyStochObj
from pystoch import PyStochCompiler

import argparse
import logging

import os
import sys
import tempfile

def run(prog, args=[], localsdict={}, verbose=False):
    if verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING
        
    logger = logging.getLogger('pystoch')
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    logger.addHandler(ch)
    logger.debug('set loglevel to %s' % loglevel)
    
    PYSTOCHOBJ = PyStochObj()

    filename = None
    tempname = None
    sys.argv = [prog] + args
    
    if prog.endswith('.pystoch'):
        filename = prog
    else:
        generator = PyStochCompiler()
        generator.compile(prog)
        source = generator.source
        temp = tempfile.NamedTemporaryFile(
            prefix='tmp_', suffix='.pystoch', dir='/tmp', delete=False)
        temp.write(source)
        temp.close()
        filename = temp.name
        tempname = temp.name

    try:
        localsdict.update({'PYSTOCHOBJ': PYSTOCHOBJ, 'sys': sys})
        execfile(filename, localsdict)
    finally:
        if tempname is not None:
            os.remove(temp.name)

    return localsdict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a PyStoch program.')
    parser.add_argument('-v', dest='verbose', default=False,
                        action='store_true', help='print debug statements')
    parser.add_argument('program', metavar='file', type=str, nargs=1,
                        help='the PyStoch file to execute')
    parser.add_argument('arguments', metavar='arg', type=str, nargs='*',
                        help='arguments to the PyStoch program')

    args = parser.parse_args()
    run(args.program[0], args=args.arguments,
        verbose=args.verbose)
    
