import lsqfitgp as lgp
import numpy as np
import gvar
import jax

hyperprior = gvar.gvar(1, 1)

def makegp(p):
    gp = lgp.GP((0.01 + p ** 2) * lgp.White(), checkpos=False, checkfinite=False, solver='chol')
    gp.addx(0, 0)
    return gp

data = {0: 1}

fit = lgp.empbayes_fit(hyperprior, makegp, data, raises=False, verbosity=3, jit=True, method='gradient', mlkw=dict(direct_autodiff=True))
