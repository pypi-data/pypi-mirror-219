import functools

class lippa:
    
    def __init__(self):
        self.impl = lambda x: x
    
    def __call__(self, arg):
        return self.impl(arg)

    def lupi(self, num):
        orig = self.impl
        transf = self.lupi.impls[num](self)
        new = lippa()
        new.impl = lambda x: transf(orig(x))
        return new
    
def impl(meth):
    oldmeth = getattr(lippa, meth.__name__)
    @functools.wraps(oldmeth)
    def newmeth(*args):
        return oldmeth(*args)
    newmeth.impls = {0: meth}
    def one(meth):
        newmeth.impls[1] = meth
        return newmeth
    newmeth.one = one
    return newmeth
    
class cippa(lippa):
    
    @impl
    def lupi(self):
        return lambda x: x
    
    @lupi.one
    def lupi(self):
        return lambda x: x ** 2

u = cippa()

print(cippa.lupi.impls[0](u)(2)) # -> 2
print(cippa.lupi.impls[1](u)(2)) # -> 4

print(u.lupi.impls[0](u)(2)) # -> 2
print(u.lupi.impls[1](u)(2)) # -> 4

print(u.lupi(0)(2)) # -> 2
print(u.lupi(1)(2)) # -> 4
