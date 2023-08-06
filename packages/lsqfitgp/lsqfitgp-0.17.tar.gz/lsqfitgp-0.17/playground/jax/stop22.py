from jax.interpreters import ad
from jax._src.ad_util import stop_gradient_p
import jax

@jax.custom_jvp
def f(x):
    return x ** 2

@f.defjvp
def f_jvp(x, t):
    return x[0], jax.lax.stop_gradient(t[0])

ad.primitive_transposes[stop_gradient_p] = lambda ct, _: [jax.lax.stop_gradient(ct)]

print(jax.grad(f)(1.)) # -> 1
print(jax.grad(jax.grad(f))(1.)) # -> 0
print(jax.jacfwd(jax.jacrev(f))(1.))
