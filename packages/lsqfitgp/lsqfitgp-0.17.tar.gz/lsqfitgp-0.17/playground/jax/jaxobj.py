import jax
import functools
import jax.test_util

@jax.tree_util.register_pytree_node_class
class Decomp:
    
    def tree_flatten(self):
        return (self.l, self.a), None
    
    @classmethod
    def tree_unflatten(cls, aux_data, children):
        self = super().__new__(cls)
        self.l, self.a = children
        return self

    # use __new__ instead of __init__ because __init__ does not return anything
    @functools.partial(jax.jit, static_argnums=0)
    def __new__(cls, a):
        self = super().__new__(cls)
        # stops a's gradient now since we are going to define custom gradients
        # w.r.t. a anyway
        self.l = jax.scipy.linalg.cholesky(jax.lax.stop_gradient(a), lower=True)
        self.a = a
        return self
    
    def solve(self, b):
        return self._solve(self, b)
    
    @jax.custom_jvp
    @staticmethod # staticmethod otherwise custom_jvp won't see self
    @jax.jit
    def _solve(self, b):
        lb = jax.scipy.linalg.solve_triangular(self.l, b, lower=True)
        llb = jax.scipy.linalg.solve_triangular(self.l.T, lb, lower=False)
        return llb
    
    @_solve.defjvp
    @jax.jit
    def _solve_jvp(primals, tangents):
        self, b = primals
        self_dot, b_dot = tangents
        a_dot = self_dot.a
        primal = self.solve(b)
        tangent_a = -self.solve(a_dot) @ primal # -a^-1 ∂a a^-1 b
        tangent_b = self.solve(b_dot)
        return primal, tangent_a + tangent_b

key = jax.random.PRNGKey(0)
m = jax.random.normal(key, (5, 5))
_, key = jax.random.split(key)
b = jax.random.normal(key, (5,))
a = m @ m.T
dec = Decomp(a)
x = dec.solve(b)
print(jax.numpy.linalg.norm(a @ x - b, 2)) # -> 3.095427e-06

# rev mode does not work, dunno why
jax.test_util.check_grads(lambda b: dec.solve(b), (b,), order=2, modes='fwd')
jax.test_util.check_grads(lambda m: Decomp(m @ m.T).solve(b), (m,), order=2, modes='fwd')
