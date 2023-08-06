import jax
from jax import tree_util

@tree_util.register_pytree_node_class
class cippa:
    
    def __init__(self, x):
        self.x = x
    
    def __repr__(self):
        return repr(self.x)
    
    def tree_flatten(self):
        return (self.x,), None
    
    @classmethod
    def tree_unflatten(cls, aux_data, children):
        self = cls.__new__(cls)
        self.x, = children
        return self

class lippa(cippa): pass

print(jax.jacfwd(lambda x: x)(cippa(0.)))
print(jax.jacfwd(lambda x: x)(lippa(0.))) # -> error, not registered
