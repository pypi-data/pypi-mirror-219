import functools

import jax
from jax import numpy as jnp

# def itertangents(args, argnum):
#     for i, x in enumerate(args):
#         if i == argnum:
#             yield jnp.ones(shape, dtype)
#         else:
#             yield jnp.zeros(shape, dtype)

def elementwise_grad(fun, argnum=0):
    assert int(argnum) == argnum and argnum >= 0, argnum
    @functools.wraps(fun)
    def funderiv(*args):
        preargs = args[:argnum]
        postargs = args[argnum + 1:]
        def oneargfun(arg):
            args = preargs + (arg,) + postargs
            return fun(*args)
        primal = args[argnum]
        shape = getattr(primal, 'shape', ())
        dtype = getattr(primal, 'dtype', type(primal))
        tangent = jnp.ones(shape, dtype)
        primal_out, tangent_out = jax.jvp(oneargfun, (primal,), (tangent,))
        return tangent_out
    return funderiv
    
x = jnp.arange(6.).reshape(2, 3)
fun = jnp.sin

print(jax.vmap(jax.vmap(jax.grad(fun), 0), 1)(x.T))
print(elementwise_grad(fun)(x))

print(jax.vmap(jax.vmap(jax.grad(jax.grad(fun)), 0), 1)(x.T))
print(elementwise_grad(elementwise_grad(fun))(x))

f = lambda x, y: 2 * x + 3 * y
print(elementwise_grad(f)(0., 0.))
print(elementwise_grad(f, 1)(0., 0.))
print(elementwise_grad(f)(jnp.zeros((1, 5)), jnp.zeros((3, 1))))
