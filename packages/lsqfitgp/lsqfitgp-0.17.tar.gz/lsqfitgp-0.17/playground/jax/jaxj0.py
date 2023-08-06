import functools

import jax
from jax import numpy as jnp
from jax import core
from jax.interpreters import ad
from jax.interpreters import batching
from jax import abstract_arrays
from scipy import special

def makejaxufunc(ufunc, *derivs):
    prim = core.Primitive(ufunc.__name__)
    
    @functools.wraps(ufunc)
    def func(*args):
        return prim.bind(*args)

    @prim.def_impl
    def impl(*args):
        return ufunc(*args)

    @prim.def_abstract_eval
    def abstract_eval(*args):
        return x

    jvps = (
        None if d is None
        else lambda g, *args: d(*args) * g
        for d in derivs
    )
    ad.defjvp(prim, *jvps)

    batching.defvectorized(prim)
    
    return func

j0 = makejaxufunc(special.j0, lambda x: -j1(x))
j1 = makejaxufunc(special.j1, lambda x: (j0(x) - jn(2, x)) / 2.0)
jn = makejaxufunc(special.jn, None, lambda n, x: (jn(n - 1, x) - jn(n + 1, x)) / 2.0)
