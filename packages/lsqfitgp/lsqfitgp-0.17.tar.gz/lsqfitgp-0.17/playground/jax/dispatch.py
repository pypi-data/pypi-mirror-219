import functools

import jax
import jax.numpy as jnp

@functools.singledispatch
def f(_):
    print('failure')

@f.register
def _(_: jnp.ndarray):
    print('success')

f(jnp.zeros(1)) # -> success

def g(x):
    f(x)
    return x

jax.jacobian(g)(jnp.zeros(1)) # -> failure
jax.jit(g)(jnp.zeros(1))
jax.jit(jax.jacobian(g))(jnp.zeros(1))

# class MyTracer(jax.core.Tracer):
#     __init__ = lambda _: None
#     aval = property(lambda _: jax.core.UnshapedArray(object))
#
# print(isinstance(MyTracer(), jnp.ndarray)) # -> True
# print(issubclass(jax.core.Tracer, jnp.ndarray)) # -> False
#
# ArrayMeta = type(jnp.ndarray)
# def __subclasscheck__(self, subclass):
#     if issubclass(subclass, jax.core.Tracer):
#         return True
#     else:
#         return super(ArrayMeta, self).__subclasscheck__(subclass)
# ArrayMeta.__subclasscheck__ = __subclasscheck__
# print(issubclass(jax.core.Tracer, jnp.ndarray)) # -> True
#
# jax.jacobian(g)(jnp.zeros(1)) # -> failure
#
# @f.register
# def _(_: jax.core.Tracer):
#     print('~success')
#
# jax.jacobian(g)(jnp.zeros(1)) # -> ~success
