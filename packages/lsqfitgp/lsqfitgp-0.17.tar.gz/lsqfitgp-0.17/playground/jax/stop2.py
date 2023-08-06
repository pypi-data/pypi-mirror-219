import jax
from jax import numpy as jnp
from jax.interpreters import ad
from jax._src.ad_util import stop_gradient_p

# ad.primitive_transposes[stop_gradient_p] = lambda ct, _: [jax.lax.stop_gradient(ct)]

@jax.custom_jvp
def stop_hessian(x):
    return x

@stop_hessian.defjvp
def stop_hessian_jvp(primals, tangents):
    x, = primals
    x_dot, = tangents
    return x, jax.lax.stop_gradient(x_dot)

def f(x):
    return jnp.sin(jnp.cos(x))

def g(x):
    return 1/2 * x ** 2

def h(x):
    return g(stop_hessian(f(x)))

# h = 1/2 f^2
# h' = f f'
# h'' = f' f' + f f'' =
#               ^^^^^ stop_hessian should remove this

x = jnp.arange(4.)
f1 = jax.vmap(jax.grad(f))
f2 = jax.vmap(jax.grad(jax.grad(f)))
print("f' f':  ", f1(x) ** 2)
print("f f'':  ", f(x) * f2(x))
print('total:  ', f1(x) ** 2 + f(x) * f2(x))
print('fwd-fwd:', jax.vmap(jax.jacfwd(jax.jacfwd(h)))(x)) # ok -> f' f'
print('rev-fwd:', jax.vmap(jax.jacrev(jax.jacfwd(h)))(x)) # ok -> f' f'
print('fwd-rev:', jax.vmap(jax.jacfwd(jax.jacrev(h)))(x)) # wrong -> f f'' (?)
print('rev-rev:', jax.vmap(jax.jacrev(jax.jacrev(h)))(x)) # wrong -> f f'' (?)
