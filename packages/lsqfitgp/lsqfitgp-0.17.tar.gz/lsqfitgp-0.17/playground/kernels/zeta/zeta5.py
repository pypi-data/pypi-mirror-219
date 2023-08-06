import itertools

import numpy as np
from matplotlib import pyplot as plt
import gvar

import lsqfitgp as lgp

fig, ax = plt.subplots(num='zeta5', clear=True)

clist = [2] # coherence length > 0
vlist = [2] # smoothness parameter >= 0
alist = [1] # seasonal variance in [0, 1]
slist = [5] # correlation length > 0

x = np.linspace(0, 10, 1001)
for c, v, a, s in itertools.product(clist, vlist, alist, slist):
    covfun = a * lgp.Zeta(nu=v) * lgp.Matern(nu=v, scale=c) + (1 - a) * lgp.Matern(nu=v, scale=s)
    gp = lgp.GP(covfun)
    gp.addx(x, 0)
    p = gp.prior(0)
    y = gvar.sample(p, eps=1e-12)
    ax.plot(x, y, label=f'c={c}, v={v}, a={a}, s={s}')

ax.legend()

fig.show()
