import jax
from jax import numpy as jnp
import numpy as np

def check_aux(aux):
    print()
    for op in [jax.grad, jax.jacrev, jax.jacfwd]:
        print(op.__name__)
        print(op(lambda x: (x, aux), has_aux=True)(0.))

@jax.tree_util.register_pytree_node_class
class cippa:

    def __init__(self, **kw):
        self.kw = kw
        self.names = None

    def tree_flatten(self):
        if self.names is None:
            self.names = [n for n, x in self.kw.items() if isinstance(x, jnp.ndarray)]
        children = tuple(self.kw[n] for n in self.names)
        return children, self.names

    @classmethod
    def tree_unflatten(cls, names, children):
        self = cls(**dict(zip(names, children)))
        self.names = names

check_aux(cippa(a='ciao'))
check_aux(cippa(a=jnp.zeros(1)))
