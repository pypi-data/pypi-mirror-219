import itertools
import functools

import jax
from jax import numpy as jnp

class logfunc:
    
    _indent = 0
    
    def __init__(self, func):
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kw):
        repr_args = map(repr, args)
        repr_kw = (f'{k}={v!r}' for k, v in kw.items())
        arglist = ', '.join(itertools.chain(repr_args, repr_kw))
        arglist = '...'
        print(4 * self._indent * ' ' + self._func.__name__ + '(' + arglist + ')')
        self.__class__._indent += 1
        try:
            result = self._func(*args, **kw)
        finally:
            self.__class__._indent -= 1
        return result

logfunc = lambda x: x

@jax.custom_jvp
@logfunc
def stop_hessian(x):
    return x

@stop_hessian.defjvp
@logfunc
def stop_hessian_jvp(p, t):
    x, = p
    xt, = t
    return x, stop_hessian_helper(x) * xt

@jax.custom_jvp
@logfunc
def stop_hessian_helper(x):
    return 1

@stop_hessian_helper.defjvp
@logfunc
def stop_hessian_helper_jvp(p, t):
    x, = p
    xt, = t
    return 0., xt

@logfunc
def f(x):
    return jnp.sin(jnp.cos(x))

@logfunc
def g(x):
    return 1/2 * x ** 2

@logfunc
def h(x):
    return g(stop_hessian(f(x)))

# h = 1/2 f^2
# h' = f f'
# h'' = f' f' + f f''
#               ^^^^^ stop_hessian should remove this

x = jnp.arange(4.)
f1 = jax.vmap(jax.grad(f))
f2 = jax.vmap(jax.grad(jax.grad(f)))

print("f' =", f1(x))
print('fwd:', jax.vmap(jax.jacfwd(lambda x: stop_hessian(f(x))))(x))
print('rev:', jax.vmap(jax.jacrev(lambda x: stop_hessian(f(x))))(x))
print()

print("f f' =", f(x) * f1(x))
print('fwd:  ', jax.vmap(jax.jacfwd(h))(x))
print('rev:  ', jax.vmap(jax.jacrev(h))(x))
print()

print("f' f' =    ", f1(x) ** 2)
print("f f'' =    ", f(x) * f2(x))
print("f'f'+ff'' =", f1(x) ** 2 + f(x) * f2(x))
print('fwd-fwd:   ', jax.vmap(jax.jacfwd(jax.jacfwd(h)))(x)) # ok -> f' f'
print('rev-fwd:   ', jax.vmap(jax.jacrev(jax.jacfwd(h)))(x)) # ok -> f' f'
print('fwd-rev:   ', jax.vmap(jax.jacfwd(jax.jacrev(h)))(x)) # wrong -> f f'' (?)
print('rev-rev:   ', jax.vmap(jax.jacrev(jax.jacrev(h)))(x)) # wrong -> f f'' (?)
