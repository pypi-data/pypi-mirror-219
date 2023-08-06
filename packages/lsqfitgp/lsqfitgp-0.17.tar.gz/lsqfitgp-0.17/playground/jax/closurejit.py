import jax

@jax.jit
def f(a, b):
    print('f: a =', a)
    print('f: b =', b)
    @jax.jit
    def g(a):
        print('g: a =', a)
        print('g: b =', b)
        return b * a
    return g(a)

print(f(2, 3))
print(f(2, 5))
