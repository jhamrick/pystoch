import _ast
import ast
import codegen
import os
import pdb
import sys

def pystoch_compile(source):
    generator = PyStochCompiler()
    generator.compile(source)
    return generator.source

class PyStochCompiler(codegen.SourceGenerator):

    def __init__(self):
        super(PyStochCompiler, self).__init__(' ' * 4, False)

        self.LINE_STACK = []
        self.FUNCTION_STACK = []

    @property
    def source(self):
        return ''.join(self.result)

    def insert(self, statements):
        for statement in statements:
            super(PyStochCompiler, self).newline()
            self.write(statement)

    def compile(self, src):
        stmts = [
            "MODULE_STACK.push('foo')", # need to pick a reasonable value here
            "LINE_STACK.push(0)",
            ""
            ]
        self.insert(stmts)

        if os.path.exists(src):
            source = open(src, 'r').read()
        else:
            source = src

        node = ast.parse(source)
        self.visit(node)

    def newline(self, node=None, extra=0):
        super(PyStochCompiler, self).newline(node=node, extra=extra)
        if node is None: return

        self.write("LINE_STACK.increment()")
        super(PyStochCompiler, self).newline()

    def body(self, statements, to_write=None):
        self.new_line = True
        self.indentation += 1
        
        if to_write is not None:
            self.insert(to_write)
        
        for stmt in statements:
            self.visit(stmt)
        self.indentation -= 1

    def body_or_else(self, node, to_write=None):
        self.body(node.body, to_write=to_write)
        if node.orelse:
            self.newline()
            self.write('else:')
            self.body(node.orelse)

    ########### Visitor Functions ###########

    def visit_FunctionDef(self, node):
        self.newline(extra=1)
        self.decorators(node)
        self.newline(node)
        self.write('def %s(' % node.name)
        self.signature(node.args)
        self.write('):')

        to_write = [
            "FUNCTION_STACK.push('foo')", # need to pick a reasonable value here
            "LINE_STACK.push(0)"
            ]

        self.body(node.body, to_write=to_write)
        self.insert(['\tFUNCTION_STACK.pop()']) # this is hacky...

    def visit_ClassDef(self, node):
        have_args = []
        def paren_or_comma():
            if have_args:
                self.write(', ')
            else:
                have_args.append(True)
                self.write('(')

        self.newline(extra=2)
        self.decorators(node)
        self.newline(node)
        self.write('class %s' % node.name)
        for base in node.bases:
            paren_or_comma()
            self.visit(base)
        # XXX: the if here is used to keep this module compatible
        #      with python 2.6.
        if hasattr(node, 'keywords'):
            for keyword in node.keywords:
                paren_or_comma()
                self.write(keyword.arg + '=')
                self.visit(keyword.value)
            if node.starargs is not None:
                paren_or_comma()
                self.write('*')
                self.visit(node.starargs)
            if node.kwargs is not None:
                paren_or_comma()
                self.write('**')
                self.visit(node.kwargs)
        self.write(have_args and '):' or ':')

        to_write = [
            "CLASS_STACK.push('foo')", # need to pick a reasonable name here
            "LINE_STACK.push(0)"
            ]
        
        self.body(node.body, to_write=to_write)

    def visit_Return(self, node):
        self.newline(node)
        self.write('return_val = ')
        self.visit(node.value)

        to_write = [
            "FUNCTION_STACK.pop()",
            "LINE_STACK.pop()",
            "return return_val"
            ]

        self.insert(to_write)
        
    def visit_For(self, node):
        self.newline(node)
        self.write("for_val = ") # probably need to pick a more reasonable value here
        self.visit(node.iter)
        self.newline(node)
        super(PyStochCompiler, self).newline()
        self.insert(["LOOP_STACK.push(0)"])
        super(PyStochCompiler, self).newline()
        self.write('for ')
        self.visit(node.target)
        self.write(' in for_val:')

        to_write = [
            "LOOP_STACK.increment()"
            ]

        self.body_or_else(node, to_write)
        self.insert(["LOOP_STACK.pop()"])

    def visit_While(self, node):
        self.newline(node)
        self.write("while_val = ") # probably need to pick a more reasonable value here
        self.visit(node.test)
        self.newline(node)
        super(PyStochCompiler, self).newline()
        self.insert(["LOOP_STACK.push(0)"])
        super(PyStochCompiler, self).newline()
        self.write('while while_val:')

        to_write = [
            "LOOP_STACK.increment()"
            ]

        self.body_or_else(node, to_write)
        self.insert("LOOP_STACK.pop()")

    def visit_ListComp(self, node):
        self.newline(node)
        self.write("listcomp = []")
        elt = node.elt

        def parse_generator(nodes):
            node = nodes[-1]
            tempnode = ast.For()
            tempnode.target = node.target
            tempnode.iter = node.iter
            # TODO: deal with ifs here...
            if len(nodes) == 1:
                gen = PyStochCompiler()
                gen.visit(elt)
                body = [ast.parse("listcomp.append(%s)" % gen.source)] # some better naming scheme here?
            else:
                body = [parse_generator(nodes[:-1])]
            tempnode.body = body
            tempnode.orelse = None
            return tempnode

        self.visit(parse_generator(node.generators))            
            
    def visit_DictComp(self, node):
        raise NotImplementedError

    def visit_Assign(self, node):
        self.newline(node)
        if isinstance(node.value, _ast.ListComp):
            self.visit(node.value)
            #print node.value

            # TODO: finish this stuff

            self.newline(node)
            for idx, target in enumerate(node.targets):
                if idx:
                    self.write(', ')
                self.visit(target)
            self.write(' = listcomp')

        else:
            super(PyStochCompiler, self).visit_Assign(node)

if __name__ == "__main__":
    infile = sys.argv[1]
    transform = pystoch_compile(infile)

    if infile.endswith(".py"):
        outfile = infile.rstrip(".py") + ".pystoch"
    else:
        outfile = infile + ".pystoch"
    
    of = open(outfile, 'w')
    of.write(transform)
    of.close()
