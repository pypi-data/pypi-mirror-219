import jax
from jax import numpy as jnp

with jax.checking_leaks():
    @jax.jit
    @jax.grad
    def test(xy):
        x, y = xy
        try:
            with jax.ensure_compile_time_eval():
                assert jnp.all(x >= 0)
                assert jnp.all(y >= 0)
        except jax.errors.ConcretizationTypeError:
            pass
        # with jax.ensure_compile_time_eval():
        #     assert jnp.all(x >= 0)
        #     assert jnp.all(y >= 0)
        return x @ y
    test((jnp.arange(8.), jnp.arange(8.)))
