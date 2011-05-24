def foo(val):
    return val
def bar(func1, func2):
    return func1(func2(10))
def baz(func):
    return 1 - func

result = bar(baz, foo)
