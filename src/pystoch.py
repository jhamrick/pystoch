import ast
import argparse

def parse(program, args):
    source = open(program, 'r').read()
    walk(ast.parse(source))

def walk(node):
    for n in ast.walk(node):
        print n

parser = argparse.ArgumentParser(description='Run a PyStoch program.')
parser.add_argument('program', metavar='file', type=str, nargs=1,
                    help='the PyStoch file to execute')
parser.add_argument('arguments', metavar='arg', type=str, nargs='*',
                    help='arguments to the PyStoch program')

args = parser.parse_args()
parse(args.program[0], args.arguments)
