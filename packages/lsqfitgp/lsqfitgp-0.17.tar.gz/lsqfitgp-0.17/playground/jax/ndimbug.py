import jax
from jax import numpy as jnp
from jax.scipy import linalg as jlinalg
import numpy

func = lambda x: x + jnp.ndim([jnp.ones(1)])
func(0.)
jax.jit(func)(0.)
