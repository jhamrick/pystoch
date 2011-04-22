import argparse
import compile

def parse(program, args):
    source = open(program, 'r').read()
    walk(ast.parse(source))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a PyStoch program.')
    parser.add_argument('program', metavar='file', type=str, nargs=1,
                        help='the PyStoch file to execute')
    parser.add_argument('arguments', metavar='arg', type=str, nargs='*',
                        help='arguments to the PyStoch program')

    args = parser.parse_args()
    parse(args.program[0], args.arguments)
    
