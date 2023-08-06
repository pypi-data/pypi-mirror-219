import jax

def f(x):
    y = 2 * x
    return y, y

g = jax.jacfwd(f, has_aux=True)

print(g(3.))
