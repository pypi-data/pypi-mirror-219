import jax
import numpy as np

def func(x):
    return x

@jax.custom_jvp
def gunc(x):
    return x

@gunc.defjvp
def gunc_jvp(p, t):
    return gunc(*p), t[0]

x = np.array(None)

func(x)
gunc(x)
