class Stack(object):

    def __init__(self):
        self.stack = []

    def pop(self):
        return self.stack.pop(0)

    def push(self, elmt):
        self.stack.insert(0, elmt)

    def increment(self):
        self.stack[0] += 1

    def decrement(self):
        self.stack[0] -= 1
