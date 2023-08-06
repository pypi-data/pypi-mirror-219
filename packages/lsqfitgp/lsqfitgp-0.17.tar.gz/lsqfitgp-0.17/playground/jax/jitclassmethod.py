import functools

import jax
from jax import numpy as jnp

class Cippa:
    
    @classmethod
    @functools.partial(jax.jit, static_argnums=(0,))
    def lippa(cls, x):
        try:
            if jnp.all(x):
                print('ciao')
        except jax.errors.ConcretizationTypeError:
            pass
        else:
            raise RuntimeError('x is static')
        return x + 1

print(Cippa.lippa(4))
print(Cippa.lippa(jnp.arange(10)))
