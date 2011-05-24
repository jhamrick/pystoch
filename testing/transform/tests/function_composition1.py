def foo():
    return 10
def bar(func):
    return func() * 10

result = bar(foo)
