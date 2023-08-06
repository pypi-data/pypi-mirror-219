import functools

class cippa: pass
class lippa: pass
class fagiolino(cippa, lippa): pass

@functools.singledispatch
def f(_):
    print('not dispatched')

@f.register
def _(_: lippa):
    print('lippa')

f(None)
f(fagiolino())
