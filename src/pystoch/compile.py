"""pystoch.compile

This module contains the operations necessary to compile a normal
python program (with stochastic function calls) into a pystoch
program.

"""

import _ast
import ast
import codegen
import datetime
import hashlib
import os
import pdb
import sys

def pystoch_compile(source):
    """Compile python to pystoch.

    Parameters
    ----------
    source : string
        If source is a valid path, it will load the source from the
        path and compile that.  If it is not, then it will be treated
        as the text of the source itself and be compiled.

    Returns
    -------
    out : string
        The compiled source

    """
    
    generator = PyStochCompiler()
    generator.compile(source)
    return generator.source

class PyStochCompiler(codegen.SourceGenerator):
    """A visitor class to transform a python abstract syntax tree into
    pystoch.

    This class inherits from pystoch.codegen.SourceGenerator, which is
    a NodeVisitor that transforms a python abstract syntax tree (AST)
    into python code.  The PyStochCompiler takes it one step further,
    overriding the appropriate functions from SourceGenerator in order
    to insert PyStoch necessary code and perform PyStoch
    transformations.

    See Also
    --------
    pystoch.codegen
    pystoch.ast
    _ast
    ast

    """

    def __init__(self):
        """Initialize the PyStochCompiler.

        This initializes the SourceGenerator, and creates a new list
        for pystoch identifiers (in order to avoid hash collisions).

        """
        
        super(PyStochCompiler, self).__init__(' ' * 4, False)
        self.idens = []
        
    def _gen_iden(self, node):
        """Generate a random unique PyStoch identifier.

        All PyStoch identifiers are prefixed by 'PYSTOCHID_', followed
        by an eight-character hexadecimal string.  The hexadecimal is
        the first eight characters of the md5 digest of the current
        date and time concatenated with the hash of `node`.

        All generated ids are stored, and if a collision is detected,
        the function will try again (with a different date and time)
        to generate a unique id.

        Parameters
        ----------
        node : ast.AST
            The node to generate an id for

        Returns
        -------
        out : string
            The identifier for `node`

        """
        
        now = str(datetime.datetime.now())
        nodeid = str(hash(node))
        iden = hashlib.md5(now + nodeid).hexdigest()[:8]
        if iden in self.idens:
            iden = self._gen_iden(node)
        self.idens.append(iden)
        return "PYSTOCHID_%s" % iden

    @property
    def source(self):
        """The source generated by the PyStochCompiler after `compile`
        has been called.

        """
        
        return ''.join(self.result)

    def insert(self, statements):
        """Insert non-node statements into the source.

        This is used for inserting non-node statements into the source
        compilation.  These generally should only be PyStoch-specific
        statements; if they are a statement that needs to be evaluated
        by the PyStoch compiler then this function should NOT be used.

        You can pass in either a list/tuple of statements, or a single
        statement.

        Parameters
        ----------
        statements : string or list or tuple
           The statement or statements to be inserted

        """

        # turn it into a list if it's not already
        if not isinstance(statements, (list, tuple)):
            statements = [statements]

        # write each statement, separated by a newline
        for statement in statements:
            super(PyStochCompiler, self).newline()
            self.write(statement)

    def compile(self, src):
        """Compile python source to pystoch source.

        Parameters
        ----------
        src : string
            If source is a valid path, it will load the source from the
            path and compile that.  If it is not, then it will be treated
            as the text of the source itself and be compiled.

        Returns
        -------
        out : string
            The compiled source

        """

        # read in the source from a file
        if os.path.exists(src):
            source = open(src, 'r').read()
        # ... or just treat src as the actual source
        else:
            source = src

        # parse the source into an AST
        node = ast.parse(source)

        # generate an identifier for the module/file, and push this
        # identifier onto the module stack.  Also push a 0 onto the
        # line stack.
        iden = self._gen_iden(node)
        self.insert([
            "MODULE_STACK.push('%s')" % iden,
            "LINE_STACK.push(0)",
            ""
            ])

        # compile the rest of the module
        self.visit(node)

        # and finally, pop the line and module stacks
        self.insert([
            "LINE_STACK.pop()",
            "MODULE_STACK.pop()",
            ""])

    def newline(self, node=None, extra=0):
        """Insert a newline.
        
        This inserts a newline in the same way as SourceGenerator,
        with the additional catch of incrementing the line stack if
        the node asking for the newline is non-null (if it's null,
        then incrementing the line stack is pointless because nothing
        will happen between now and the next time a newline occurs).

        Parameters
        ----------
        node : ast.AST (default=None)
            The ast node to insert a newline for
        extra : integer (default=0)
            The number of extra newlines to insert

        Notes
        -----
        This function doesn't actually immediately insert a newline,
        it increments the number of newlines to insert and then
        inserts them when write() is called.

        """
        
        # call the parent newline method
        super(PyStochCompiler, self).newline(node=node, extra=extra)
        # return if the node is null
        if node is None: return

        # otherwise, incremet the line stack and then insert another
        # newline
        self.write("LINE_STACK.increment()")
        super(PyStochCompiler, self).newline(node=node, extra=extra)

    def body(self, statements, write_before=None, write_after=None):
        """Write the body statements.

        This is the same as the SourceGenerator body function, with
        the additional parameters of write_before and write_after.
        These parameters allow you to insert extra stuff before and
        after the rest of the statements.

        Parameters
        ----------
        statements : list of ast.AST nodes
            The statements to be written in the body
        write_before : list or string
            The statements to write before the body
        write_after : list or string
            The statements to write after the body

        """

        # increment the level of indentation
        #self.new_line = True
        self.indentation += 1

        # insert the write_before statementss
        if write_before is not None:
            self.insert(write_before)

        # write the actual body statements
        for stmt in statements:
            self.visit(stmt)

        # insert the write_after statements
        if write_after is not None:
            self.insert(write_after)

        # decrement the level of indentation
        self.indentation -= 1

    def body_or_else(self, node, write_before=None, write_after=None):
        """Write a body as well as an else statement, if it exists.

        Parameters
        ----------
        node : ast.AST
            node that has a body and optionally an orelse
        write_before : list or string
            The statements to write before the body
        write_after : list or string
            The statements to write after the body

        See Also
        --------
        pystoch.compile.PyStochCompiler.body

        """
        
        self.body(node.body, write_before=write_before, write_after=write_after)
        if node.orelse:
            self.newline()
            self.write('else:')
            self.body(node.orelse)

    def to_assign(self, value):
        """Takes a value, creates a random temporary identifier for
        it, and creates an Assign node, assigning the value to the
        identifier.

        Parameters
        ----------
        value : ast.AST
            node that is to be the value of the Assign node

        Returns
        -------
        out : tuple of string, _ast.Assign
            the string is the identifier of the node, and the
            _ast.Assign is the node that was created

        """
        
        iden = self._gen_iden(value)
        node = _ast.Assign()
        node.targets = [ast.parse(iden).body[0].value]
        node.value = value
        return iden, node

    def contains_call(self, node):
        """Checks whether or not a node (_ast.AST) contains any Call nodes.

        Parameters
        ----------
        node : _ast.AST
            The node to check for Call nodes

        Returns
        -------
        out : boolean
            Whether or not the node contains any Call nodes

        """

        def iter_fields(node):
            """Iterate over all fields of a node, only yielding
            existing fields.

            """
            for field in node._fields:
                try:
                    yield field, getattr(node, field)
                except AttributeError:
                    pass

        class CallChecker(ast.NodeVisitor):
            def visit_Call(self, node):
                return True

            def generic_visit(self, node):
                for field, value in iter_fields(node):
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, _ast.AST):
                                if self.visit(item):
                                    return True
                    elif isinstance(value, _ast.AST):
                        if self.visit(value):
                            return True

                return False

        cc = CallChecker()
        return cc.visit(node)

    ########### Visitor Functions ###########

    # 1) Statements

    def visit_FunctionDef(self, node):
        """Rewrite the FunctionDef visitor to push a new value onto
        the function and line stacks at the beginning of the function,
        and then pop those values at the end of the function.

        """
        
        self.newline(extra=1)
        self.decorators(node)
        self.newline(node)
        self.write('def %s(' % node.name)
        self.signature(node.args)
        self.write('):')

        write_before = [
            "FUNCTION_STACK.push('%s')" % self._gen_iden(node),
            "LINE_STACK.push(0)"
            ]

        write_after = [
            "LINE_STACK.pop()",
            "FUNCTION_STACK.pop()"
            ]

        self.body(node.body, write_before=write_before, write_after=write_after)

    def visit_ClassDef(self, node):
        """Rewrite the ClassDef visitor to push new values onto the
        class and line stacks at the beginning of the stack, and then
        to pop those values at the end of the class.

        """
        
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

        write_before = [
            "CLASS_STACK.push('%s')" % self._gen_iden(node),
            "LINE_STACK.push(0)"
            ]

        write_after = [
            "",
            'LINE_STACK.pop()',
            'CLASS_STACK.pop()',
            ""
            ]
        
        self.body(node.body, write_before=write_before, write_after=write_after)

    def visit_Return(self, node):
        """Rewrite the Return visitor function to first store the
        return value of the function, then pop the line and function
        stacks, then return the stored value.

        TODO: This should somehow make sure that the line and function
        stacks aren't popped again after the return statement.

        """

        # store the value of the return statement in `iden`
        iden, assignment = self.to_assign(node.value)
        self.visit(assignment)

        # pop the line and function stacks, then return the stored
        # value
        self.insert([
            "LINE_STACK.pop()",
            "FUNCTION_STACK.pop()",
            "return %s" % iden
            ])

    def visit_Delete(self, node):
        super(PyStochCompiler, self).visit_Delete(node)
        
    def visit_Assign(self, node):
        """Rewrite the Assign visitor function to deal with list
        comprehensions.

        TODO: this should also deal with compound and nested function
        calls

        """
        
        if isinstance(node.value, _ast.ListComp):
            iden = self.visit(node.value)
            self.newline(node)
            for idx, target in enumerate(node.targets):
                if idx:
                    self.write(', ')
                self.visit(target)
            self.write(' = %s' % iden)

        else:
            super(PyStochCompiler, self).visit_Assign(node)

    def visit_AugAssign(self, node):
        raise NotImplementedError
        
    def visit_Print(self, node):
        # XXX: python 2.6 only
        self.newline(node)
        self.write('print ')
        want_comma = False
        if node.dest is not None:
            self.write(' >> ')
            self.visit(node.dest)
            want_comma = True
        for value in node.values:
            if want_comma:
                self.write(', ')
            self.visit(value)
            want_comma = True
        if not node.nl:
            self.write(',')

    def visit_For(self, node):
        """Rewrite the For visitor function to first store the
        iterator of the for loop in a temporary variable, and then to
        loop over the contents of that variable.  Additionally, push a
        new value onto the loop stack before entering the for loop,
        increment that value after each pass of the loop, and pop the
        value after the loop has terminated.

        """
        
        # store the value of the iterator for the for loop
        iden, assignment = self.to_assign(node.iter)
        self.visit(assignment)

        # push a new value onto the loop stack
        self.newline(node)
        super(PyStochCompiler, self).newline()
        self.insert(["LOOP_STACK.push(0)"])
        super(PyStochCompiler, self).newline()

        # iterate over the stored value for the for loop iterator
        self.write('for ')
        self.visit(node.target)
        self.write(' in %s:' % iden)

        # increment the loop stack at the end of the body
        self.body_or_else(node, write_before="LOOP_STACK.increment()")
        
        # and finally, pop the loop stack after the for loop is over
        self.insert("LOOP_STACK.pop()")

    def visit_While(self, node):
        """Rewrite the While visitor function to first store the test
        of the while loop in a temporary variable, and then to loop
        over the contents of that variable.  Additionally, push a new
        value onto the loop stack before entering the while loop,
        increment that value after each pass of the loop, and pop the
        value after the loop has terminated.

        """

        # store the value of the test case for the while loop
        iden, assignment = self.to_assign(node.test)
        self.visit(assignment)

        # push a new value onto the loop stack
        self.newline(node)
        super(PyStochCompiler, self).newline()
        self.insert(["LOOP_STACK.push(0)"])
        super(PyStochCompiler, self).newline()

        # iterate over the stored test case
        self.write('while %s:' % iden)

        # increment the loop stack at the end of the body
        self.body_or_else(node, write_before="LOOP_STACK.increment()")

        # and finally, pop the loop stack at the end of the body
        self.insert("LOOP_STACK.pop()")

    def visit_If(self, node):
        """Rewrite the If visitor function to assign the if and elif
        tests to temporary variables, and then check these variables
        in the actual if and elif statements.

        """

        # store the if test in a temporary variable
        ifiden, assignment = self.to_assign(node.test)
        self.visit(assignment)

        # store each of the elif tests in temporary variables
        orig_node = node
        elif_idens = []
        while True:
            else_ = node.orelse
            if len(else_) == 1 and isinstance(else_[0], _ast.If):
                node = else_[0]
                iden, assignment = self.to_assign(node.test)
                elif_idens.append(iden)
                self.visit(assignment)
            else:
                break

        # set the node back to the original node, and actually create
        # the if statement using the temporary variable name
        node = orig_node
        self.newline(node)
        self.write('if %s:' % ifiden)
        self.body(node.body)

        # create the rest of the elifs using their temporary variable
        # names, if they exist, and create the else statement if it
        # exists
        i = 0
        while True:
            else_ = node.orelse
            if len(else_) == 1 and isinstance(else_[0], _ast.If):
                node = else_[0]
                self.newline()
                self.write('elif %s:' % elif_idens[i])
                self.body(node.body)
                i += 1
            else:
                self.newline()
                self.write('else:')
                self.body(else_)
                break

    def visit_With(self, node):
        raise NotImplementedError

    def visit_Raise(self, node):
        raise NotImplementedError

    def visit_TryExcept(self, node):
        raise NotImplementedError

    def visit_TryFinally(self, node):
        raise NotImplementedError

    def visit_Assert(self, node):
        raise NotImplementedError

    def visit_Import(self, node):
        super(PyStochCompiler, self).visit_Import(node)

    def visit_ImportFrom(self, node):
        super(PyStochCompiler, self).visit_ImportFrom(node)

    def visit_Exec(self, node):
        """Exec statements are not supported at this time.

        """
        
        raise NotImplementedError, "Exec statements are not supported at this time"

    # 2) Expressions

    def visit_BoolOp(self, node):
        raise NotImplementedError

    def visit_BinOp(self, node):
        raise NotImplementedError

    def visit_UnaryOp(self, node):
        raise NotImplementedError

    def visit_Lambda(self, node):
        raise NotImplementedError

    def visit_IfExp(self, node):
        raise NotImplementedError

    def visit_Dict(self, node):
        raise NotImplementedError

    def visit_Set(self, node):
        raise NotImplementedError

    def visit_ListComp(self, node):
        """Rewrite the ListComp visitor function to turn the list
        comprehension into a real for loop.  This is necessary to be
        able to correctly label any random functions that get called
        from within the list comprehension.  Basically, this function
        creates a temporary variable for the list, and transforms the
        comprehension into a for loop that appends values onto this
        list.  The list name is then returned, so that whatever
        element called the for loop can handle the assignment
        properly.

        """
        
        # make an identifier for the list
        self.newline(node)
        iden = self._gen_iden(node)
        self.write("%s = []" % iden)
        elt = node.elt

        def parse_generator(nodes):
            """Transform the generator into a for loop.

            """
            
            node = nodes[-1]
            tempnode = ast.For()
            tempnode.target = node.target
            tempnode.iter = node.iter
            # TODO: deal with ifs here...
            if len(nodes) == 1:
                iden2, assignment = self.to_assign(elt)
                body = [assignment, 
                        ast.parse("%s.append(%s)" % (iden, iden2))]
            else:
                body = [parse_generator(nodes[:-1])]
                
            tempnode.body = body
            tempnode.orelse = None
            return tempnode

        # visit the for loop
        self.visit(parse_generator(node.generators))

        # return the identifier of the list we created
        return iden
            
    def visit_SetComp(self, node):
        """Set comprehensions are not supported at this time.

        """

        raise NotImplementedError, "Set comprehensions are not supported at this time"

    def visit_DictComp(self, node):
        """Dictionary comprehensions are not supported at this time.

        """
        
        raise NotImplementedError, "Dictionary comprehensions are not supported at this time"

    def visit_GeneratorComp(self, node):
        raise NotImplementedError

    def visit_Yield(self, node):
        raise NotImplementedError

    def visit_Compare(self, node):
        raise NotImplementedError

    def visit_Call(self, node):
        raise NotImplementedError

    def visit_Attribute(self, node):
        raise NotImplementedError

    def visit_Subscript(self, node):
        raise NotImplementedError

    def visit_List(self, node):
        raise NotImplementedError

    def visit_Tuple(self, node):
        raise NotImplementedError

    # 3) Misc

    def visit_Slice(self, node):
        raise NotImplementedError

    def visit_Index(self, node):
        raise NotImplementedError

if __name__ == "__main__":
    # TODO: this should do some real argument parsing
    
    infile = sys.argv[1]
    transform = pystoch_compile(infile)

    if infile.endswith(".py"):
        outfile = infile.rstrip(".py") + ".pystoch"
    else:
        outfile = infile + ".pystoch"
    
    of = open(outfile, 'w')
    of.write(transform)
    of.close()
